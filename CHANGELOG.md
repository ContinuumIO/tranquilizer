# Changelog

## [0.1.0] - 2018-09-28
### Added
- Support for sphinx `:param:`, `:raises:` in swagger documentation
- Exceptions return a 500 status code

### Changed
- Removed custom types from `__init__.py`
- Support common datayptes: `list()`, `typing.List[]`, `datetime.datetime`, `datetime.date`.
- Support file handles: `typing.BinaryIO` and `typing.TextIO`
- Support images and arrays: `PIL.Image.Image`, `numpy.ndarray`
