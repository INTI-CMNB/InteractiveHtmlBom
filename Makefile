#!/usr/bin/make
PY_COV=python3-coverage

deb:
	fakeroot dpkg-buildpackage -uc -b

deb_clean:
	fakeroot debian/rules clean

lint:
	# flake8 --filename is broken
	# stop the build if there are Python syntax errors or undefined names
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --statistics

test:
	$(PY_COV) erase
	pytest-3
	$(PY_COV) report


.PHONY: deb deb_clean
