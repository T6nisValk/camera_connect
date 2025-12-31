# Changelog

All notable changes to Simple Importer will be documented in this file.

## [1.3.0] - 2025-12-31

### Added

- Settings dialog for configuring source and output paths
- Settings dialog for selecting file types (JPG/RAW)
- Persistent settings saved to settings.json file
- Confirmation dialog before import showing selected settings
- Validation to ensure at least one file type is selected
- Error handling for missing files and invalid JSON settings

### Changed

- Removed file type checkboxes from main window
- Settings now loaded from settings.json instead of GUI state
- Improved error messaging when no files are found to import

### Fixed

- Import button now correctly shows "Copy" action in confirmation dialog
- Import and delete button correctly shows "Move" action in confirmation dialog
- Import button now re-enables properly when errors occur
- Folder browse dialogs now preserve previous value when cancelled

## [1.2.0] - 2025-12-30

### Added

- Option to move (cut) images instead of copying them
- Copy/Move toggle functionality in the interface

## [1.1.0] - Previous Release

### Added

- Initial release
- Import pictures from camera
- Organize images by capture date
- Separate RAW and JPG files into dedicated folders
- Support for .arw, .jpg, and .jpeg file formats
