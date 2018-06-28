# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright 2018 Anaconda, Inc.
#
# All Rights Reserved.
# -----------------------------------------------------------------------------
from version import find_version
from setuptools import setup, find_packages


setup(
    name='comatose',
    author='Albert DeFusco',
    author_email='adefusco@anaconda.com',
    description='Serve REST API using decorated functions',
    url='https://github.com/ContinuumIO/Comatose',
    license='MIT',
    version=find_version('comatose', '__init__.py'),
    packages=find_packages(),
    entry_points={
        #'anaconda_project.plugins.command_run': [
        #    'rest_api = comatose.__main__:init_command',
        #],
        'console_scripts': [
            'comatose = comatose.__main__:main'
        ]
    },
    scripts=[]
)
