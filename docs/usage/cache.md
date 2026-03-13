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
        configure_cache(ckan_config, 'example')
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
