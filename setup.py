import versioneer
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires=[
    'flask',
    'werkzeug>=0.15,<2.0',
    'flask-restx',
    'flask-cors',
    'python-dateutil',
    'flask-jwt-extended>=4'
]

extras_require={
    'recommended': [
        'nbconvert',
        'ipython',
        'numpy',
        'pillow'
    ]
}

extras_require['all'] = sorted(set(sum(extras_require.values(), [])))

setup(
    name='tranquilizer',
    author='Albert DeFusco',
    author_email='albert.defusco@me.com',
    description='Put your functions to REST',
    url='https://github.com/AlbertDeFusco/tranquilizer',
    license='BSD 3-clause',
    platforms=['Windows', 'Mac OS X', 'Linux'],
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'tranquilizer = tranquilizer.main:run'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: BSD License",
        "Framework :: Flask",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Environment :: Web Environment"
    ],
    python_requires=">=3.6, <3.10",
    install_requires=install_requires,
    extras_require=extras_require,
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown'

)

