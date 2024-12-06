# template-python-package

This is a template repository for python packages.
This template uses [Poetry](https://python-poetry.org/docs/#installation)

## Using this repository
1. Update the name of the project in:
    - README.md
    - pyproject.toml
    - Rename the main project folder 
2. Remove this section of the README 

## Local development

### Setup

Start Poetry with the following command

```shell
poetry shell
```

Install dependencies

```shell
poetry install
```

### Updating Python Dependencies

Update all python dependencies to latest compatible versions

```shell
poetry update
```

Add a new dependency with optional dev flag. Updates the lock file and installs the new dependency

```shell
poetry add <package_name>@<package_version> [--dev]
```

### Testing

Tests can be run by using the `invoke` task.

```shell
poetry run pytest
poetry run pytest -k TestMyService  # Run a specific test or test suite
```
