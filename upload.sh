#!/bin/bash

# brew install pandoc
pandoc --from=markdown --to=rst --output=readme.rst readme.md
python setup.py register -r pypi
python setup.py sdist upload -r pypi
