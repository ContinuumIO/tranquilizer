# Changelog

## [0.7.0] - 2021-12-13

### Added
- JWT opaque token support with `--secret-key <secret-key>`

### Changed
- Dropped Python 3.5
- Validated support for Python 3.9

## [0.6.0] - 2021-06-07
### Added
- CORS support using `--allow-origin HOST:PORT` or `$TRANQUILIZER_ALLOW_ORIGIN`

### Fixed
- Example in README

## [0.5.0] - 2020-07-20
### Changed
- Migrated from flask-restplus to flask-restx
- Relax werkzeug pin to allow version 1.x

## [0.4.1] - 2019-12-22
### Fixed
- Fixed tranquilizer.__version__

## [0.4.0] - 2019-09-30
### Changed
- Added Python 3.7 support (rewrite type checking)
- Utilize Versioneer

### Added
- anaconda-enterprise @publish compatiblity
- @publish: When methods is set un-typed arguments are returned
  as a list-of-strings.
- nearly complete test coverage
- Travis CI

## [0.3.3] - 2019-09-06
## Changed
- Fixed ProxyFix call for werkzeug>=0.15

## [0.3.2] - 2019-05-30
### Changed
- Updated setup.py to include more classifiers and requirements
- Python 3.7 typing.List and derivatives does not work

## [0.3.1] - 2019-03-13
### Changed
- Report when nbconvert is not installed, but needed

## [0.3.0] - 2019-03-06
### Changed
- pillow and numpy not required

## [0.2.1] - 2019-03-06
### Added
- Set maximum content length for all endpoints
- Allow --port, --address, and --prefix arguments

## [0.2.0] - 2019-01-23
### Added
- Support serving from Jupyter Notebooks

## [0.1.2] - 2018-12-29
### Added
- Customize application name in Swagger with `--name`

## [0.1.1] - 2018-10-26
- Add `--version`

## [0.1.0] - 2018-09-28
### Added
- Support for sphinx `:param:`, `:raises:` in swagger documentation
- Exceptions return a 500 status code

### Changed
- Removed custom types from `__init__.py`
- Support common datayptes: `list()`, `typing.List[]`, `datetime.datetime`, `datetime.date`.
- Support file handles: `typing.BinaryIO` and `typing.TextIO`
- Support images and arrays: `PIL.Image.Image`, `numpy.ndarray`
