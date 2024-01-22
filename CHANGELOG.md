# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Note: only changes after the fork are listed.


## [Unreleased]

## [2.8.1-1] - 2024-01-22
### Added
- Better support for KiCad 7.99
- Toggle to hide top bar
- Implement untented vias for kicad
- KiCad 7 native dnp field support
    
### Fixed
- Handling empty string for board variant
- Tracks sometimes overlapping via holes
- Handling of complex polygonpours
- Extra data file change not updating fields

## [2.7.0-1] - 2022-08-01
### Added
- Reset button for settings/checkboxes
- Configurable net colors

### Changed
- Limit fields grid max height

### Fixed
- Support for current KiCad 7.99
- Minor dialog UI details
- Filter not working when extra fields are ints

## [2.6.0-1] - 2022-03-30
### Added
- Support for current KiCad 7.99

### Changed
- Suppressed some distracting messages

## [2.5.0-3] - 2022-02-15
### Added
- Create hyperlinks for URLs
- Support for more KiCad 7 new stuff

## [2.5.0-2] - 2022-10-24
### Added
- Offset back rotation 180 degrees option
- Natural integer sorting for extra fields

### Fixed
- Import settings
- DNP and board variant field doesn't need to be specified in extra fields

## [2.5.0] - 2022-06-13
### Added
- Hotkeys link and rotate board with l/r arrows
- CSV/TXT export according to #289
- Implement local/global settings

### Fixed
- Rectangles in angled footprints
- Compatibility with wxWidgets 3.1.6

### Changed
- Resize plugin icon to 24x24 and pixel align again

## [2.4.1-4] - 2022-05-20
### Added
- Command line option for version

## [2.4.1-3] - 2022-04-25
### Fixed
- Problems with dimensions in the Edge.Cuts layer

## [2.4.1-2] - 2022-04-23
### Fixed
- No text variables expansion in title_block.date

## [2.4.1] - 2021-12-23
### Added
- Better KiCad 6 support
- Expand text vars in title block
- Support for Eagle / Fusion 360 Electronics
- Support for arc tracks
- Description field parsing
- Compression is now optional
- BoM Column hiding and reordering
- Darken when checked highlights footprints on render
- Resizable column border
- Configurable grouping
- Sort references intelligently 

### Changed
- Standard fields optional

### Fixed
- Grouping issues
- Workaround for lower canvas not drawn on print

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


