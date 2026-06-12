# !/usr/bin/env python
# encoding: utf-8

import copy
import inspect

from beaker.cache import CacheManager, cache_regions
from ckan.plugins import toolkit


def get_cache_opts(ext_name, cache_names=None, ckan_config=None):
    """
    Loads options from the config.

    :param ext_name: the name of the extension (without the ckanext-)
    :param cache_names: load options for these named regions. If not specified, options
        will be loaded for one region with the ext_name as the name.
    :param ckan_config: (optional) CKAN config. If not provided, toolkit.config will be
        used.
    """
    ckan_config = ckan_config or toolkit.config
    if cache_names is not None and isinstance(cache_names, str):
        cache_names = [cache_names]
    elif cache_names is None:
        cache_names = [ext_name]
    default_opts = {}
    region_overrides = {}
    for k, v in ckan_config.items():
        if k.startswith(f'ckanext.{ext_name}.cache.'):
            keys = k.split('.')[3:]
            if keys[0] == '_region':
                region_name = keys[1]
                if region_name not in cache_names:
                    continue
                region_opts = region_overrides.get(region_name, {})
                region_opts[keys[-1]] = v
                region_overrides[region_name] = region_opts
            else:
                default_opts[keys[-1]] = v
    opts = {}
    for region_name in cache_names:
        region_opts = copy.deepcopy(default_opts)
        region_opts.update(region_overrides.get(region_name, {}))
        opts[region_name] = region_opts
    return opts


def configure_cache(ckan_config, ext_name, cache_names=None):
    """
    Configures beaker cache regions using settings from the CKAN config.

    Use in plugin.py:IConfigurable.configure().

    :param ckan_config: CKAN config from configure()
    :param ext_name: the name of the extension (without the ckanext-)
    :param cache_names: create these named regions. If not specified, one region will be
        created using the ext_name.
    """
    opts = get_cache_opts(ext_name, cache_names=cache_names, ckan_config=ckan_config)
    for cache_name, cache_opts in opts.items():
        cache_regions.update({cache_name: cache_opts})


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
        cache_opts = get_cache_opts(ext_name, cache_name).get(cache_name, {})
    # cache_managers does not usually seem to be populated so just construct a new ref
    cache_manager = CacheManager(**cache_opts)

    cached_functions = []

    def _is_cached_func(f):
        is_func = inspect.isfunction(f)
        has_ns = hasattr(f, '_arg_namespace')
        in_rg = getattr(f, '_arg_region', None) == cache_name
        return is_func and has_ns and in_rg

    def _get_funcs(obj, parent_module=None):
        parent_module = parent_module or obj
        funcs = []
        sub_objects = inspect.getmembers(
            obj, lambda x: inspect.getmodule(x) == parent_module
        )
        for _, so in sub_objects:
            if so == obj:
                continue  # to avoid infinite recursion
            if _is_cached_func(so):
                funcs.append(so)
            elif inspect.isclass(so):
                funcs += _get_funcs(so, parent_module)
        return funcs

    for module in modules:
        cached_functions += _get_funcs(module)

    for func in cached_functions:
        # each function has its own namespace that needs to be cleared
        try:
            cache = cache_manager.get_cache(func._arg_namespace)
            cache.clear()
        except Exception as e:
            raise CacheClearError(f'Failed to clear cache for {func.__name__}') from e


class CacheClearError(Exception):
    pass
