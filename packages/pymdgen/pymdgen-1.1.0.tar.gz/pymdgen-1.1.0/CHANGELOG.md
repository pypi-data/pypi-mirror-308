# Changelog


## Unreleased


## 1.1.0
### Added
- python3.10 support
- python3.11 support
- python3.12 support
### Removed
- python3.7 support
- python3.6 support


## 1.0.0
### Added
- python3.7 support (#12)
- python3.8 support (#12)
- python3.9 support (#12)
### Changed
- use poetry for package management (#13)
- github workflows (#13)
### Removed
- python2.7 support (#12)
- python3.4 support (#12)
- python3.5 support (#12)


## 0.2.3
### Fixed
- fix #11: ```sh code block for command output


## 0.2.2
### Fixed
- fix #8: separate section for classes and functions
- fix #10: Function spec needs to work correctly for decorated functions (py3 only)


## 0.2.1
### Added
- check for existance of `pymdgen_type_info` when documenting class attributes


## 0.2.0
### Added
- fix #5: instanced attributes section
- fix #7: add class methods


## 0.1.1
### Added
- fix #2: only generate docs for classes and functions defined in the targeted module
- fix #4: Class docs: Recognize properties that have a `help` attribute
### Fixed
- fix #3: include module name and docstring