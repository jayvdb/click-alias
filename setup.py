#!/usr/bin/env python

from setuptools import setup

with open('README.rst') as f:
    readme = f.read()

setup(
    name='click-alias',
    version='0.1.1.a3',
    description='Click command aliaser',
    long_description=readme,
    author='Hot Off The Hamster',
    author_email='hotoffthehamster@gmail.com',
    url='https://github.com/hotoffthehamster/click-alias',
    license='MIT',
    packages=['click_alias'],
    install_requires=[
        'click>=7.0',
    ],
    extras_require={
        'dev': [
            'flake8',
            'flake8-import-order',
            'tox-travis',
            'pytest',
            'pytest-cov',
            'coveralls',
            'wheel',
        ]
    }
)
