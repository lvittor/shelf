---
title: "Makefile basic usage"
draft: false
type: docs
---

<!-- 
TODO:
    1) Check if ```make clean``` is removing files which are never created by the project and remove that files in the makefile.

COMMENTS:
    1) If an "Unhashable Type" error occurs, it refers to a bug that can be solved by updating poetry's version.
       Issue: https://github.com/python-poetry/poetry/issues/2340
 -->

- [Makefile basic usage](#makefile-basic-usage)
  - [Listing available commands](#listing-available-commands)
  - [Cleaning files](#cleaning-files)
  - [Code formatting with black and isort](#code-formatting-with-black-and-isort)
  - [Running tests](#running-tests)
  - [Building the docker images](#building-the-docker-images)
  - [Removing the docker images](#removing-the-docker-images)
  - [Getting into the docker containers](#getting-into-the-docker-containers)
  - [List containers and images](#list-containers-and-images)

## Makefile basic usage

The [makefile](makefile) is used for boostup the development workflow

### Listing available commands

```bash
$ make # you can also use: make list
build_dev
build_prod
clean
docker_lsc
docker_lsi
format
list
prune
rmi
run_dev
run_prod
test
```

### Cleaning files

To clean the project files use

```bash
make clean
```

### Code formatting with black and isort

To format the code in [shelf/](shelf) and [tests/](tests) use

```bash
make format
```

This command will first do a ```make clean``` and then format the code with the black and isort settings in [pyproject.toml](pyproject.toml)

### Running tests

To run all the tests in [tests/](tests) use

```bash
make test
```

### Building the docker images

To build a desired stage use

```bash
make build_dev # build development image
```

or

```bash
make build_prod # build production image
```

### Removing the docker images

To delete the development and production images

```bash
make rmi
```

Also, you can remove all images without at least one container associated to them

```bash
make prune
```

### Getting into the docker containers

To run the container from the docker image use

```bash
make run_dev # run development container (shelf:test)
```

or

```bash
make run_prod # run production container (shelf:latest)
```

### List containers and images

To list up to 10 last created docker containers

```bash
make docker_lsc
```

Also, you can list the docker images with

```bash
make docker_lsi
```
