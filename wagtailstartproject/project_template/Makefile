.PHONY: test clean unittests chrometests firefoxtests coveragetest coverage flaketest checkmanifest checksetup install-pipeline

test: coveragetest flaketest checkmanifest checksetup

clean:
	# Erase previous coverage results
	coverage erase

unittests:
	# Run unit tests with coverage
	coverage run --append runtests.py tests.test_{{ project_name }}
	coverage combine

chrometests:
	# Run Chrome selenium tests
	coverage run --append runtests.py tests.test_selenium
	coverage combine

firefoxtests:
	# Run Firefox selenium tests
	coverage run --append runtests.py tests.test_selenium_firefox
	coverage combine

coveragetest: clean unittests chrometests firefoxtests
	# Generate coverage report and require minimum coverage
	coverage report

coverage: clean unittests chrometests firefoxtests
	# Generate test coverage html report
	coverage html
	@echo "Coverage report is located at ./var/htmlcov/index.html"

flaketest:
	# Check syntax and style
	flake8

checkmanifest:
	# Check if all files are included in the sdist
	check-manifest

checksetup:
	# Check longdescription and metadata
	python setup.py check -msr

devinstall:
	# First activate your virtual env and the correct node version
	# Then install, compile, and collect.
	pip install --upgrade -e .
	pip install --upgrade -r requirements-dev.txt
	yarn
	./manage.py collectstatic --noinput --link --clear

install-pipeline:
	pip install -e .
	@echo "===== PACKAGE DEPENDENCIES ====="
	@pip freeze | grep -ve "^-e" | sed 's/^/  /'
	@echo "================================"
	pip install -r requirements-dev.txt
