# Changelog

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
