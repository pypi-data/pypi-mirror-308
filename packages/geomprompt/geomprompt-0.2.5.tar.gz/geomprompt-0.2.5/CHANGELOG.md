# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.5] - 2024-09-17

### Added

- Additional documentation.
- Unit tests for ridge_prompt class and functions.

### Fixed

- RidgePrompts initialization with an image works properly now.

## [0.2.4] - 2024-03-08

### Added

- IO functions for saving/retrieval of SAM Automask outputs and associeated experiments (with metadata).

## [0.2.3] - 2024-03-04

### Added 
- Example experiment notebook using the PRMI data source. 

## [0.2.2] - 2024-02-29

### Added

- Ability to specify a desired number of prompt points in ridge (and valley) prompt generation.

### Removed

- Direct access to earlier prompt filtering hyperparameters (ccf and min_area).

## [0.2.1] - 2024-02-28

### Added

- Functionality in ridge prompter to also include valley prompts in case relativey darker image regions should be segmented.

### Fixed

- Fixed a bug with scaling ridge point prompts for SAM AutoMaskGenerator to image size.

### Removed

## [0.2.0] - 2024-02-27

### Added

- Ported functionality for ridge detection and point prompt derivations into project.

### Fixed

### Removed

## [0.1.0] - 2024-02-22

### Added

- Initialized project using [GDA-Cookiecutter](https://gitlab.geomdata.com/geomdata/gda-cookiecutter)

### Fixed

### Changed

### Removed
