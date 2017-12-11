.PHONY: test unittests coveragetest coverage flaketest checkmanifest checksetup install-pipeline

test: coveragetest flaketest checkmanifest checksetup

unittests:
	# Run unit tests with coverage
	coverage run setup.py test

coveragetest: unittests
	# Generate coverage report and require minimum coverage
	coverage report

coverage: unittests
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

install-pipeline:
	pip install -r requirements-dev.txt
