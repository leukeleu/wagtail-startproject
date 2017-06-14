.PHONY: test unittests coveragetest coverage flaketest checkmanifest checksetup install-pipeline

test: coveragetest flaketest checkmanifest checksetup

unittests:
	# Run unit tests with coverage
	coverage run --branch --source={{ project_name }},pages,search,tests setup.py test

coveragetest: unittests
	# Generate coverage report and require minimum coverage
	coverage report --show-missing

coverage: unittests
	# Generate test coverage html report
	coverage html

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
