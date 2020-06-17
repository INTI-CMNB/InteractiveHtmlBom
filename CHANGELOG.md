# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Note: only changes after the fork are listed.


## [Unreleased]

## [2.3.1] - 2020-06-16
### Added
- Custom js css and header/footer support

### Changed
- No to avoid X11 dependency in the pure command line tool you must define:
  INTERACTIVE_HTML_NO_X11=True

### Fixed
- The local copy of the scripts now has priority over the installed ones.
- Double click not working with "darken when checked" (#156)
- Exception when setlocale failed
- Text rendering fixes
-- process overbars
-- approximate italics behavior better

## [2.3.1] - 2020-04-24
### Added
- An option to grey out (darken) a row when the selected checkbox is checked.
- Fullscreen option to the settings menu.
- Debian package.

### Fixed
- Cleanup html settings menu


