# Auth

Loading auth functions is similar to actions, i.e. use the `@auth` decorator.

The decorator has three args, all of which are optional:

- `proxy`: the name of an existing auth function to call that function first
- `keymapping`: if the keys are different between this auth function and the proxy auth function, use this to rename them
- `anon`: boolean, if true, apply the `toolkit.auth_allow_anonymous_access` decorator.

```python
# logic/auth/module_name.py

from ckantools.decorators import auth

# all of the args are optional
@auth(anon=True)
def example_action(context, data_dict):
    # no proxy
    # anonymous access is allowed
    # then the custom auth logic:
    return {'success': data_dict.get('parameter_2') == 'carrots'}

# with args
@auth('example_action', {'param_1': 'parameter_2'})
def other_action(context, data_dict):
    # checks access to example_action first
    # the arg param_1 from this action is the same as parameter_2 in example_action (not all args/parameters have to be mapped, just the relevant ones)
    # anonymous access is not allowed
    # if it passes all that:
    return {'success': True}
```

This decorator can also be used for chained auth functions:

```python
# logic/auth/module_name.py

from ckan.plugins import toolkit
from ckantools.decorators import auth

@auth()
@toolkit.chained_auth_function
def core_ckan_action(next_auth, context, data_dict):
    return next_auth
```

The auth functions can then be loaded in `plugin.py`:
```python
# plugin.py

from .logic.auth import module_name
from ckantools.loaders import create_auth
from ckan.plugins import implements, interfaces, SingletonPlugin

class ExamplePlugin(SingletonPlugin):
    implements(interfaces.IActions)

    # IAuthFunctions
    def get_auth_functions(self):
        return create_auth(module_name)
```

Multiple auth modules can also be passed:
```python
...
    # IAuthFunctions
    def get_auth_functions(self):
        from .logic.auth import create, update, delete
        return create_auth(create, update, delete)
```

Main benefits to using the decorator:

- reduces repetition of complex auth logic
- as with the action decorator, it's neater and easier to maintain than having to list out all of the auth functions to load
