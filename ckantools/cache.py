# !/usr/bin/env python
# encoding: utf-8

import inspect

from beaker.cache import CacheManager, cache_regions
from ckan.plugins import toolkit


def configure_cache(ckan_config, ext_name, cache_name=None):
    """
    Configures a beaker cache region using settings from the CKAN config.

    Use in plugin.py:IConfigurable.configure().

    :param ckan_config: CKAN config from configure()
    :param ext_name: the name of the extension (without the ckanext-)
    :param cache_name: a name for the cache region, if different from the ext_name
    """
    options = {}
    for k, v in ckan_config.items():
        if k.startswith(f'ckanext.{ext_name}.cache.'):
            options[k.split('.')[-1]] = v
    cache_name = cache_name or ext_name
    cache_regions.update({cache_name: options})


def clear_cache_region(ext_name, *modules, cache_name=None):
    """
    Clears cached functions in the given cache region.

    :param ext_name: the name of the extension (without the ckanext-)
    :param modules: modules containing cached functions
    :param cache_name: a name for the cache region, if different from the ext_name
    """
    cache_name = cache_name or ext_name
    cache_opts = cache_regions.get(cache_name)
    if cache_opts is None:
        # this shouldn't happen, but just in case
        cache_opts = {}
        for k, v in toolkit.config.items():
            if k.startswith(f'ckanext.{ext_name}.cache.'):
                cache_opts[k.split('.')[-1]] = v
    # cache_managers does not usually seem to be populated so just construct a new ref
    cache_manager = CacheManager(**cache_opts)

    cached_functions = []

    for module in modules:

        def _is_cached_func(f):
            is_func = inspect.isfunction(f)
            has_ns = hasattr(f, '_arg_namespace')
            in_rg = getattr(f, '_arg_region', None) == cache_name
            return is_func and has_ns and in_rg

        cached_functions += inspect.getmembers(module, _is_cached_func)

    for _, func in cached_functions:
        # each function has its own namespace that needs to be cleared
        try:
            cache = cache_manager.get_cache(func._arg_namespace)
            cache.clear()
        except Exception as e:
            raise CacheClearError(f'Failed to clear cache for {func.__name__}') from e


class CacheClearError(Exception):
    pass
