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
        'console_scripts': [
            'tranquilizer = tranquilizer.__main__:main'
        ]
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Framework :: Flask"
    )

)

