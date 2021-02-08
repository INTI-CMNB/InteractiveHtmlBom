# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Note: only changes after the fork are listed.


## [Unreleased]

## [2.3.4-2] - 2021-02-08
### Changed
- Debian dependencies to accept kicad-nightly

## [2.3.4] - 2020-12-29
### Added
- Symbolic link support (#213).

### Changed
- Middle mouse button canvas panning, now matches Pcbnew and Eeschema.
- Deleted Chinese language (#153) (was broken).
- Use KiCad's own text rendering when possible.

### Fixed
- Catch exceptions on parsing net/xml files (Fixes #166)
- Return with error level != 0 for parsing errors.
- Many details to support KiCad nightly.

## [2.3.3] - 2020-06-27
### Fixed
- variants-blacklist, variants-whitelist cli options (#162)

## [2.3.2] - 2020-06-17
### Added
- Custom js css and header/footer support

### Changed
- Removed X11 dependency when DISPLAY isn't defined

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


