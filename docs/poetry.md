---
title: "Poetry basic usage"
draft: true
type: docs
---

<!--
TODO:
    1) Here you can list all the TODO's

COMMENTS:
    1) Here you can list all the COMMENTS's
 -->

- [Poetry basic usage](#poetry-basic-usage)

## Poetry basic usage

Poetry is necessary for running the [makefile](makefile). However, it is not necessary to add new dependencies, if you want to build the project read the [makefile docs](docs/makefile.md).

You should not use ```poetry install``` to install the packages in local. Instead, you can run ```make build``` to create a docker image with the required packages.

For more information about using poetry read [poetry docs](https://python-poetry.org/docs/cli/).
