#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

# dataclasses were introduced in Python3.7, if running on 3.6.* install the backport
requirements = ['dataclasses;python_version<"3.7"' ]

test_requirements = ['pytest>=3', ]

setup(
    author="Kolokotronis Panagiotis",
    author_email='panagiks@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="YAAB aims to provide a flexible base for Adapter Design Pattern implementations based on dataclasses.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='yaab',
    name='yaab',
    packages=find_packages(include=['yaab', 'yaab.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/panagiks/yaab',
    version='0.2.2',
    zip_safe=False,
)
