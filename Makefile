ifeq ($(origin .RECIPEPREFIX), undefined)
  $(error This Make does not support .RECIPEPREFIX. Please use GNU Make 4.0 or later)
endif
.RECIPEPREFIX = >

default: check

test:
> poetry run python -m pytest

install:
> poetry install -v

update:
> poetry update

remove-env:
> poetry env remove python3

deploy: clean
> python3 -m pip install --user .

build: clean
> poetry build

mypy:
> poetry run mypy nordvpn/

flake:
> poetry run flake8 nordvpn/ tests/

isort:
> poetry run isort nordvpn/ tests/

black:
> poetry run black nordvpn/ tests/

format: isort black

lint: flake mypy

check: install format lint test

ci: check build

clean:
> rm -rf *egg-info
> rm -rf build/
> rm -rf dist/
> find . -name '*.pyc' -exec rm -f {} +
> find . -name '*.pyo' -exec rm -f {} +
> find . -name '*~' -exec rm -f  {} +
> find . -name '__pycache__' -exec rm -rf  {} +
> find . -name '_build' -exec rm -rf  {} +
> find . -name '.mypy_cache' -exec rm -rf  {} +
> find . -name '.pytest_cache' -exec rm -rf  {} +

.PHONY: test lint format install build deploy ci check mypy flake isort black remove-env update
