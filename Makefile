#!/usr/bin/make
PY_COV=python3-coverage
CWD := $(abspath $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST))))))
USER_ID=$(shell id -u)
GROUP_ID=$(shell id -g)
PYTEST=pytest-3


deb:
	DEB_BUILD_OPTIONS=nocheck fakeroot dpkg-buildpackage -uc -b

deb_sig:
	DEB_BUILD_OPTIONS=nocheck fakeroot dpkg-buildpackage -b

deb_clean:
	fakeroot debian/rules clean
	rm -rf dist/ InteractiveHtmlBom.egg-info/

lint:
	# flake8 --filename is broken
	# stop the build if there are Python syntax errors or undefined names
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --statistics

test:
	$(PY_COV) erase
	$(PYTEST)
	$(PY_COV) report

test_local:
	rm -rf output
	$(PY_COV) erase
	$(PYTEST) --test_dir output
	$(PY_COV) report
	$(PY_COV) html
	x-www-browser htmlcov/index.html

single_test:
	rm -rf pp
	-$(PYTEST) --log-cli-level debug -k "$(SINGLE_TEST)" --test_dir pp
	@echo "********************" Output
	@cat pp/*/output.txt
	@echo "********************" Error
	@cat pp/*/error.txt

test_build:
	docker run --rm -v $(CWD)/..:$(CWD)/.. --workdir="$(CWD)" \
	--user $(USER_ID):$(GROUP_ID) \
	--volume="/etc/group:/etc/group:ro" \
	--volume="/etc/passwd:/etc/passwd:ro" \
	--volume="/etc/shadow:/etc/shadow:ro" \
	setsoft/kicad_pybuild:latest \
		/bin/bash -c "make deb ; make deb_clean"

test_build_shell:
	docker run --rm -it -v $(CWD)/..:$(CWD)/.. --workdir="$(CWD)" \
	--user $(USER_ID):$(GROUP_ID) \
	--volume="/etc/group:/etc/group:ro" \
	--volume="/etc/passwd:/etc/passwd:ro" \
	--volume="/etc/shadow:/etc/shadow:ro" \
	setsoft/kicad_pybuild:latest \
		/bin/bash


.PHONY: deb deb_clean
