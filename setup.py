# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright 2018 Anaconda, Inc.
#
# All Rights Reserved.
# -----------------------------------------------------------------------------
import versioneer
from setuptools import setup, find_packages
from setuptools.command.develop import VersionlessRequirement, develop as DevelopCommand


class FixedDevelopCommand(DevelopCommand):
    def install_script(self, dist, script_name, script_text, dev_path=None):
        DevelopCommand.install_script(self, VersionlessRequirement(dist), script_name, script_text, dev_path)


cmdclass = versioneer.get_cmdclass()
cmdclass['develop'] = FixedDevelopCommand

setup(
    name='comatose',
    author='Albert DeFusco',
    author_email='adefusco@anaconda.com',
    description='',
    url='https://github.com/ContinuumIO/Comatose',
    version=versioneer.get_version(),
    cmdclass=cmdclass,
    packages=find_packages(),
    namespace_packages=['comatose'],
    include_package_data=True,
    zip_safe=False,
    package_data={},
    entry_points={
        'anaconda_project.plugins.command_run': [
            'rest_api = comatose.application:init_command',
        ],
    },
    scripts=[])
