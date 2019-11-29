#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

setup_requirements = ['pytest-runner',]

setup(
    author="Han Zhichao",
    author_email='superhin@126.com',
    description='Session scope fixture "db" for mysql query or change',
    long_description='Session scope fixture "db" for mysql query or change',
    classifiers=[
        'Framework :: Pytest',
        'Programming Language :: Python',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.7',
    ],
    license="MIT license",
    include_package_data=True,
    keywords=[
        'pytest', 'py.test', 'db', 'mysql'
    ],
    name='pytest-db',
    packages=find_packages(include=['pytest_db']),
    setup_requires=setup_requirements,
    url='https://github.com/hanzhichao/pytest-db',
    version='0.1',
    zip_safe=True,
    install_requires=[
        'pytest',
        'pytest-runner',
        'pymysql'
    ],
    entry_points={
        'pytest11': [
            'pytest-db = pytest_db.plugin',
        ]
    }
)
