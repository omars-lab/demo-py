SHELL := /bin/bash
MAKEFILE_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
ENV := demopy
CONDA_HOME := $(shell which conda)
PIP := $(shell dirname $(shell dirname ${CONDA_HOME}))/envs/${ENV}/bin/pip
PYTHON := $(shell dirname $(shell dirname ${CONDA_HOME}))/envs/${ENV}/bin/python
JUPYTER := $(shell dirname $(shell dirname ${CONDA_HOME}))/envs/${ENV}/bin/jupyter
DISTRIBUTION_NAME = $(shell python setup.py --name)
DISTRIBUTION_VERSION = $(shell python setup.py --version)

include Makefile-examples

env.teardown:
	conda env remove -n ${ENV} || true

env.setup:
	conda create -n ${ENV} python=3.9 pip -y || true
	${PIP} install -e ".[dev]"

env.activate:
	@echo 'conda activate ${ENV}'

install:
	${PIP} install -e ".[dev]"
	${PIP} install -e ".[notebooks]"
	${PIP} install -e ".[chatgpt]"

clean:
	true

start.notebooks:
	cd notebooks && ${JUPYTER} notebook

lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	mypy \
		--ignore-missing-imports \
		--follow-imports=skip \
		--strict-optional \
		perfpy

build.alpha: clean
	${PYTHON} setup.py egg_info --tag-build a$(shell \
		curl https://pypi.org/pypi/${DISTRIBUTION_NAME}/json | \
		jq '[ \
			.releases | \
			to_entries[] | \
			.key | \
			select(. | contains("${DISTRIBUTION_VERSION}a")) | \
			ltrimstr("${DISTRIBUTION_VERSION}a") | \
			tonumber \
		] | sort | \
		last // 0 | \
		. + 1' \
	) sdist bdist_wheel

dev.push: build.alpha
	twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

simulate.github.secret:
	@echo 'PYPI_TOKEN='$$(cat secret.txt | base64)
