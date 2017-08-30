from setuptools import find_packages, setup

setup(
    name='{{ project_name }}',
    version='1.0.0',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    url='',
    author='',
    author_email='',
    maintainer='',
    maintainer_email='',
    description='',
    long_description=open('README.rst').read(),
    keywords=['wagtail'],
    classifiers=[
        'Programming Language :: Python',
        'License :: Other/Proprietary License'
    ],
    license='Proprietary',
    install_requires=[
        'Django',
        'wagtail',
        'psycopg2',
        'whitenoise',
    ],
    test_suite='runtests.runtests',
)
