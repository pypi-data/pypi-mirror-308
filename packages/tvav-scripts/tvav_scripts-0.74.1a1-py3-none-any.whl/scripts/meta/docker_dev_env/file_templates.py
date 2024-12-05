README_CONTENT = """
# {package_src}

## Contributing

Use the docker dev environment by running `make dev`

> Open PR and do git merge squash on approval.

> Use CI/CD for versioning, commit following these rules

> Do not modify pyproject.toml version manually.
"""
POETRY_CONTENT = """
[tool.poetry]
name = "{package_src}"
version = "0.0.1"
description = ""
authors = ["TVAV-team <tvav-sw@bmat.com>"]
maintainers = ["TVAV-team <tvav-sw@bmat.com>"]
readme = "README.md"
packages = [
    {{ include = "{package_src}" }}
]

[tool.poetry.dependencies]
python = ">=3.9,<4.0.0"

[tool.poetry.group.dev]
optional = true

[tool.poetry.group.dev.dependencies]
ruff = "0.0.278"
ipdb = "0.13.13"
factory-boy = "3.2.1"

[tool.poetry.group.test]
optional = true

[tool.poetry.group.test.dependencies]
pytest = "7.4.0"
pytest-cov = "4.1.0"
pytest-xdist = "3.3.1"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

[[tool.poetry.source]]
name = "tvav"
url = "https://installer:installer@extrapypi.tvav.bmat.com/simple/"
priority = "supplemental"

[[tool.poetry.source]]
name = "PyPI"
priority = "primary"
"""
ENV_CONTENT = """
DOCKER_CONTAINER_NAME={package_src}

# Local Registry
REGISTRY=localhost
REGISTRY_PORT=5000

# Mock database
MOCK_DATABASE=True
TEST_DATABASE_NAME=test
"""
DOCKERFILE_CONTENT = """
FROM public.ecr.aws/docker/library/python:3.9

RUN mkdir -p /src
WORKDIR /src

RUN pip install "poetry>=1.5.1,<1.6"

COPY poetry.lock /src/poetry.lock
COPY pyproject.toml /src/pyproject.toml
COPY {package_src} /src/{package_src}
COPY README.md /src/README.md

RUN poetry config virtualenvs.create false
RUN poetry install --with dev,test

RUN ipython profile create
COPY ipython_config.py /root/.ipython/profile_default/ipython_config.py

ENV PYTHONPATH .
# Docker dev env
CMD ["tail", "-f", "/dev/null"]
"""
DOCKER_COMPOSE_CONTENT = """
version: "3.7"
services:
  {package_src}:
    container_name: ${{DOCKER_CONTAINER_NAME}}
    hostname: ${{DOCKER_CONTAINER_NAME}}
    restart: always
    image: ${{REGISTRY}}:${{REGISTRY_PORT}}/${{DOCKER_CONTAINER_NAME}}_image
    env_file:
      - .env
    volumes:
      - ./:/src/
    logging:
      driver: 'json-file'
      options:
        max-size: 50m
        max-file: '2'
"""
MAKEFILE_CONTENT = """
#!make
include .env
SHELL := /bin/bash

# Constants
TAIL_LOGS = 50
PYTEST_WORKERS = 8

# Local develop
dev: complete-build sh
complete-build: build up activate-autohooks

up:
\tdocker compose up --force-recreate -d

down:
\tdocker compose down

down-up: down up

start-registry:
\tdocker run -d -p ${{REGISTRY_PORT}}:5000 --restart=always --name "${{REGISTRY_NAME}}" registry:2

build: aws-logout aws-login
\tdocker buildx build --platform linux/amd64 --output type=docker -t ${{DOCKER_CONTAINER_NAME}}_image .
\tdocker tag ${{DOCKER_CONTAINER_NAME}}_image ${{REGISTRY}}:${{REGISTRY_PORT}}/${{DOCKER_CONTAINER_NAME}}_image

activate-autohooks:
\t# TODO Add autohooks
\t# docker exec -it ${{DOCKER_CONTAINER_NAME}} poetry run autohooks activate --mode poetry --force

sh:
\tdocker exec -it ${{DOCKER_CONTAINER_NAME}} bash

logs:
\tdocker logs --tail ${{TAIL_LOGS}} -f ${{DOCKER_CONTAINER_NAME}}

# Get the aws login token. For internal use. Also needed to access internal aws images
aws-login:
\t@aws ecr get-login-password --region eu-west-1  | docker login --username AWS --password-stdin 086064441816.dkr.ecr.eu-west-1.amazonaws.com

aws-logout:
\tdocker logout public.ecr.aws
"""
DRONE_CONTENT = """
kind: pipeline
type: kubernetes
name: default

steps:
  - name: tests-and-linters
    image: public.ecr.aws/docker/library/python:3.9
    pull: if-not-exists
    commands:
      - export MOCK_DATABASE=True
      - export TEST_DATABASE_NAME=test-{package_src}
      - pip install "poetry>=1.5.1,<1.6"
      - poetry config virtualenvs.create false
      - poetry install --with dev,test
      - ruff check .
      - pytest --cov={package_src} --maxfail=5 -n 8 -vv -s --log-cli-level=ERROR --disable-pytest-warnings
    when:
      event:
        - push
        - tag

  - name: tag-commit
    image: public.ecr.aws/docker/library/python:3.11
    pull: if-not-exists
    commands:
      - echo "Generating new version + tagging"
      - pip install cicd-scripts --trusted-host extrapypi.tvav.bmat.com --extra-index-url https://installer:installer@extrapypi.tvav.bmat.com/simple/
      - python -m cicd_scripts -u -b "${{DRONE_BRANCH}}"
    when:
      event:
        - push
      branch:
        - master
    depends_on:
      - tests-and-linters

  - name: publish-package
    image: public.ecr.aws/docker/library/python:3.11
    pull: if-not-exists
    commands:
      - echo "Publishing {package_src}@${{DRONE_TAG}}"
      - pip install "poetry>=1.5.1,<1.6"
      - poetry config virtualenvs.create false
      - poetry config repositories.tvav http://extrapypi.tvav.bmat.com/simple/
      - poetry config http-basic.tvav $PYPI_USERNAME $PYPI_PASSWORD
      - poetry publish -r tvav --build
    environment:
      PYPI_USERNAME:
        from_secret: pypi_username
      PYPI_PASSWORD:
        from_secret: pypi_password
    when:
      event:
        - tag
    depends_on:
      - tests-and-linters
"""
IPYTHON_CONFIG_CONTENT = """
c = get_config()  # noqa
c.InteractiveShellApp.exec_lines = [
    "%autoreload 2",  # Allow autoreload for the shell
]
c.InteractiveShellApp.extensions = [
    "autoreload",
]
"""
GITIGNORE_CONTENT = """
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

venv/
dist/

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# PEP 582; used by e.g. github.com/David-OConnor/pyflow
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# Code editors
.vscode

# pycharm
.idea

.DS_Store
.python-version
.ruff_cache
"""
CICD_SCRIPTS_CONTENT = """
---
# Check https://bitbucket.org/bmat-music/cicd_scripts/src/master/CICD_SCRIPTS_CONFIG.md
options:
  pyproject_update: true
  readme_update: true
  tagging: true
badges:
  - title: Extrapypi version
    pattern: >
      [![{{title}}]
      (https://img.shields.io/badge/{{package_name_url}}-{{new_version}}-informational)]
      (https://extrapypi.tvav.bmat.com/dashboard/{{package_name}}/)
  - title: Build Status
    pattern: >
      [![{{title}}]
      (https://av-cicd.bmat.com/api/badges/bmat-music/{{repo_name}}/status.svg)]
      (https://av-cicd.bmat.com/bmat-music/{{repo_name}})
  - title: Python version
    pattern: >
      ![{{title}}]
      (https://img.shields.io/badge/Python-{{python_version}}-informational)
  - title: Autohooks
    pattern: >
      ![{{title}}]
      (https://img.shields.io/badge/autohooks-{{autohooks_plugins}}-red)
variables:
  repo_name: {package_src}
  autohooks_plugins: no
regexp_variables:
  - name: package_name
    match_pattern: 'name = \\"(.*)\\"'
    replace: []
  - name: package_name_url
    match_pattern: 'name = \\"(.*)\\"'
    replace:
      - old_value: '-'
        new_value: '--'
      - old_value: '_'
        new_value: '__'
      - old_value: ' '
        new_value: '_'
  - name: python_version
    match_pattern: 'python = \\"(.*)\\"'
    replace:
      - old_value: '>='
      - old_value: ',<4.0.0'
        new_value: '+'
  - name: autohooks_plugins
    match_pattern: 'pre-commit = \\[(.*)\\]'
    replace:
      - old_value: 'autohooks.plugins.'
      - old_value: '"'
      - old_value: ', '
        new_value: '|'
"""

FILE_CONTENT_MAPPINGS = [
    ("README.md", README_CONTENT),
    ("pyproject.toml", POETRY_CONTENT),
    (".env", ENV_CONTENT),
    ("Dockerfile", DOCKERFILE_CONTENT),
    ("docker-compose.yml", DOCKER_COMPOSE_CONTENT),
    ("Makefile", MAKEFILE_CONTENT),
    (".drone.yml", DRONE_CONTENT),
    ("ipython_config.py", IPYTHON_CONFIG_CONTENT),
    (".gitignore", GITIGNORE_CONTENT),
    ("config/cicd_scripts.yml", CICD_SCRIPTS_CONTENT),
]

CLIENT_FOLDER_STRUCTURE = (
    "{package_src}/common/__init__.py",
    "{package_src}/backend/__init__.py",
    "{package_src}/aggregations/__init__.py",
    "{package_src}/match_importer/__init__.py",
    "{package_src}/cuenator/__init__.py",
    "{package_src}/cuesheet_importer/__init__.py",
    "{package_src}/processor/__init__.py",
    "{package_src}/reports/__init__.py",
)
