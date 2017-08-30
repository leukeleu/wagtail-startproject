.PHONY: test flaketest checkmanifest checksetup

test: flaketest checkmanifest checksetup

flaketest:
	# Check syntax and style
	flake8

checkmanifest:
	# Check if all files are included in the sdist
	check-manifest

checksetup:
	# Check longdescription and metadata
	python setup.py check -msr
