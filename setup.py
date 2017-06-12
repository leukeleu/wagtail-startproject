import io

from setuptools import find_packages, setup

setup(
    name='wagtailstartproject',
    version='0.1.4',
    description='This app contains a custom project template and a custom wagtail start command to allow creating customized wagtail setups',
    long_description=io.open('README.rst', encoding='utf-8').read(),
    keywords=['wagtail', 'startproject',],
    author='Ramon de Jezus (Leukeleu)',
    author_email='rdejezus@leukeleu.nl',
    maintainer='Leukeleu',
    maintainer_email='info@leukeleu.nl',
    url='https://github.com/leukeleu/wagtail-startproject',
    packages=find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    license='MIT',
    install_requires=[
        'django',
    ],
    include_package_data=True,
    zip_safe=False,
    entry_points="""
            [console_scripts]
            wagtail_startproject=wagtailstartproject.wagtailstartproject:main
    """
)
