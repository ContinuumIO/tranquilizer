from version import find_version
from setuptools import setup, find_packages

setup(
    name='tranquilizer',
    author='Albert DeFusco',
    author_email='adefusco@anaconda.com',
    description='Put your functions to REST',
    url='https://github.com/ContinuumIO/tranquilizer',
    license='BSD 3-clause',
    version=find_version('tranquilizer', '__init__.py'),
    packages=find_packages(),
    entry_points={
        #'anaconda_project.plugins.command_run': [
        #    'tranquilizer_api = tranquililizer.__main__:init_command',
        #],
        'console_scripts': [
            'tranquilizer = tranquilizer.__main__:main'
        ]
    }
)

