# Actions

Use the `@action` decorator to add actions:
```python
# logic/actions/module_name.py

from ckantools.decorators import action

schema = {
        'parameter_1': [not_missing, str],
        'parameter_2': [ignore_missing, int_validator]
    }

helptext = 'This action only exists as an example, so does not actually do anything.'

@action(schema, helptext, get=False, other_decorator_1, other_decorator_2)
def example_action(parameter_1, parameter_2):
    # ...
```

Or the `@basic_action` decorator if you want to load the action but don't want any of the other features (schema loading, auto auth, etc):
```python
from ckantools.decorators import basic_action

@basic_action
@toolkit.chained_action
def example_action(next_func, context, data_dict):
    # ...
```

And then load the action(s) in `plugin.py`:
```python
# plugin.py

from .logic.actions import module_name
from ckantools.loaders import create_actions
from ckan.plugins import implements, interfaces, SingletonPlugin

class ExamplePlugin(SingletonPlugin):
    implements(interfaces.IActions)

    # IActions
    def get_actions(self):
        return create_actions(module_name)
```

Main benefits to using the decorator:

- automatically calls relevant auth function
- injects items defined in schema as function args
- allows you to define long or complex schemas and helptexts without cluttering up code and/or affecting readability
- neater and easier to maintain than having to list out all of the actions you want to load, e.g.
  ```python
        ## IActions
  def get_actions(self):
    return {
        'example_action': module_name.example_action,
        'other_action': module_name.other_action,
        'other_other_action': module_name.other_other_action,
        # etc
    }
  ```
