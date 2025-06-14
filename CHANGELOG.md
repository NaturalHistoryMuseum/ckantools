## v0.4.2 (2025-06-03)

### Fix

- accept 3 args for auth functions

### Docs

- improve decorator docs

### Style

- run automated fixes

### CI System(s)

- update workflows
- update pre-commit config and switch to ruff

### Chores/Misc

- remove old dist files

## v0.4.1 (2023-12-04)

### Fix

- return settings even if they're false

## v0.4.0 (2023-12-04)

### Feature

- add functions to get settings from ckan config

### Fix

- cast debug value as bool

### Chores/Misc

- add build info to rtd config

## v0.3.3 (2023-12-01)

### Fix

- **actions**: add kw to action_function

### Build System(s)

- add sync workflow to keep branches updated
- update docs, pre-commit config, and repo health files

## v0.3.2 (2022-11-24)

### Fix

- add cz-nhm extra requirement to bump flow

### Docs

- add logo
- improve docs styling and content
- add docs with mkdocs

### Build System(s)

- use cz_nhm commitizen config
- add mkdocs config to rtd config

### CI System(s)

- add patch bump

### Chores/Misc

- **commits**: move cz config into separate file
- add to gitignore

## v0.3.1 (2022-11-03)

### Fix

- update version in pyproject.toml and add version_files

## v0.3.0 (2022-11-02)

### Feat

- **utils**: add utils module

## v0.2.0 (2022-10-28)

### Feat

- **decorators**: allow multiple proxies

## v0.1.0 (2022-10-27)

### Feat

- **actions**: add basic_action to load action via decorator without schema etc
- **vars**: add vars file for common constants, variables, etc

## v0.0.7 (2022-10-26)

### Fix

- **decorators**: hotfix to convert decorator tuple into list

## v0.0.6 (2022-10-25)

### Fix

- **decorators**: revert back to loading other decorators within action decorator

## v0.0.5 (2022-10-25)

### Fix

- **decorators**: add other attributes back onto wrapped function

## v0.0.4 (2022-10-24)

## v0.0.3 (2022-10-03)

## v0.0.2 (2022-06-09)

### Feat

- attempt to create auth and validator loaders as well
- adding some of the methods from vds

## v0.0.1 (2022-06-06)

### Feat

- initial commit
