# Changelog

All notable changes to PyFAEST will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.1] - 2025-12-01

### Fixed
- Improved bundled library detection in faest_build.py to verify actual library files exist
- Fixed PyPI installation failure where bundled libraries were not properly detected
- Package now installs correctly from PyPI without external dependencies

## [1.0.0] - 2025-12-01

### Added
- Initial release of PyFAEST
- Python bindings for all 12 FAEST parameter sets
  - FAEST-128F, FAEST-128S (NIST Level 1)
  - FAEST-192F, FAEST-192S (NIST Level 3)
  - FAEST-256F, FAEST-256S (NIST Level 5)
  - FAEST-EM-128F, FAEST-EM-128S (Extended Mode, Level 1)
  - FAEST-EM-192F, FAEST-EM-192S (Extended Mode, Level 3)
  - FAEST-EM-256F, FAEST-EM-256S (Extended Mode, Level 5)
- Key generation, signing, and verification
- Key serialization and deserialization
- Memory-safe private key handling with automatic clearing
- Type-safe API with input validation
- Comprehensive test suite (37 tests)
- Example scripts demonstrating all features
- Full documentation
- Bundled FAEST library support for PyPI distribution
- Automatic platform detection for bundled libraries
- Scripts for preparing releases and updating libraries
- Comprehensive publishing guide

### Changed
- Build script now prioritizes bundled libraries over external paths
- Updated setup.py for PyPI packaging with bundled libraries

### FAEST Library Version
- Based on FAEST reference implementation v2.0.4
- Compiled from faest-ref main branch

### Platform Support
- Linux x86_64 (WSL and native)
- Python 3.7 through 3.12

### Known Limitations
- Currently supports Linux only (WSL for Windows users)
- macOS and native Windows support planned for future releases
