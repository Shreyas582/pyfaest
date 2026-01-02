# Changelog

All notable changes to PyFAEST will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v1.0.18] - 2026-01-02

### Added
- **Linux aarch64 (ARM64) support** - Pre-built wheels for Raspberry Pi, AWS Graviton, and other ARM64 Linux systems
- **macOS x86_64 (Intel Mac) support** - Pre-built wheels for Intel-based Macs
- Cross-compilation in CI for all new platforms

### Changed
- Expanded platform support from 2 to 4 architectures
- Improved `faest_build.py` platform detection with architecture normalization
- Updated CI workflow to build wheels for all supported platforms

### Fixed
- Fixed aarch64 cross-compilation by disabling OpenSSL (uses SHAKE-based randomness)
- Fixed CI workflow arm64 repository configuration issue

### Platform Support Summary
- ✅ Linux x86_64 - Pre-built wheels
- ✅ Linux aarch64 - Pre-built wheels (NEW)
- ✅ macOS arm64 - Pre-built wheels
- ✅ macOS x86_64 - Pre-built wheels (NEW)
- ✅ Windows via WSL - Use Linux wheels

## [v1.0.17] - 2026-01-02

### Added
- **Linux aarch64 (ARM64) support** - Pre-built wheels for Raspberry Pi, AWS Graviton, and other ARM64 Linux systems
- **macOS x86_64 (Intel Mac) support** - Pre-built wheels for Intel-based Macs
- Cross-compilation in CI for all new platforms

### Changed
- Expanded platform support from 2 to 4 architectures
- Improved `faest_build.py` platform detection with architecture normalization
- Updated CI workflow to build wheels for all supported platforms

### Fixed
- Fixed aarch64 cross-compilation by disabling OpenSSL (uses SHAKE-based randomness)

### Platform Support Summary
- ✅ Linux x86_64 - Pre-built wheels
- ✅ Linux aarch64 - Pre-built wheels (NEW)
- ✅ macOS arm64 - Pre-built wheels
- ✅ macOS x86_64 - Pre-built wheels (NEW)
- ✅ Windows via WSL - Use Linux wheels

## [1.0.15] - 2025-12-03

### Added
- Initial stable release of PyFAEST
- Pre-built wheels for Python 3.8-3.14 on Linux x86_64 and macOS arm64
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
- Bundled FAEST libraries in source distribution
- Automatic platform detection for bundled libraries
- Scripts for preparing releases and updating libraries

### Fixed
- Modern PEP 517 compliant wheel building with `pip wheel`
- Missing dependencies (wheel, cffi, pycparser) now properly installed
- Removed Python 3.7 support (EOL and unavailable on modern runners)

### FAEST Library Version
- Based on FAEST reference implementation v2.0.4
- Compiled from faest-ref main branch

### Platform Support
- ✅ Linux x86_64 - Pre-built wheels, no compilation required
- ✅ macOS arm64 - Pre-built wheels, no compilation required
- ✅ Windows via WSL - Use Linux wheels in WSL environment
- Python 3.8, 3.9, 3.10, 3.11, 3.12, 3.13, 3.14-dev

### Known Limitations
- Windows native support not included (use WSL)
- macOS x86_64 (Intel) not included (builds timeout on CI, use source install or Rosetta 2)
- Source builds available as fallback for unsupported platforms
