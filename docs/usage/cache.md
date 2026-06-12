# Cache

`ckantools.cache` includes functions for configuring and clearing a beaker cache region associated with an extension.

## `configure_cache`

`configure_cache` is intended to be used in the `.configure()` hook of the `IConfigurable` interface, e.g.

```python
# plugin.py

from ckantools.cache import configure_cache
from ckan.plugins import implements, interfaces, SingletonPlugin

class ExamplePlugin(SingletonPlugin):
    implements(interfaces.IConfigurable)

    # IConfigurable
    def configure(self, ckan_config):
        # this will create one cache region called 'example'
        configure_cache(ckan_config, 'example')
```

It loads `.cache` settings from the CKAN config, e.g.:

```ini
# config.ini

ckanext.example.cache.type = ext:redis
ckanext.example.cache.url = redis://your-redis-ip:1234/0
ckanext.example.cache.expire = 60
```

### Multiple regions

You can also define multiple regions and override the default settings in the config:

```ini
# config.ini

ckanext.example.cache.type = ext:redis
ckanext.example.cache.url = redis://your-redis-ip:1234/0
ckanext.example.cache._region.example_short.expire = 60
ckanext.example.cache._region.example_long.expire = 604800
```

Then load with:

```python
# plugin.py

def configure(self, ckan_config):
    # creates two regions called 'example_short' (expire time 60s) and 'example_long' (expire time 604800s)
    # these regions use the default .cache settings that aren't overridden (i.e. type and url in this example)
    # the default 'example' region is not created
    configure_cache(ckan_config, 'example', ['example_short', 'example_long'])
```


## `clear_cache_region`

`clear_cache_region` clears the associated region wherever it is required. It only clears cached functions in the modules passed to it.

e.g. to clear whenever packages are created:

```python
# plugin.py

from .lib import cached_utils
from .other_module import other_module_with_cached_functions
from ckantools.cache import clear_cache_region
from ckan.plugins import implements, interfaces, SingletonPlugin

class ExamplePlugin(SingletonPlugin):
    implements(interfaces.IPackageController)

    # IPackageController
    def after_create(self, context: dict, pkg_dict: dict):
        clear_cache_region('example', cached_utils, other_module_with_cached_functions)
```
