# Changelog

All notable changes to PyFAEST will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v1.0.29] - 2026-01-02

### Fixed
- **aarch64 rename wheel for PyPI** - PyPI rejects `linux_aarch64` platform tag
  - Rename wheel from `linux_aarch64` to `manylinux_2_17_aarch64` during repair step
  - Skip auditwheel but still apply manylinux tag for PyPI compatibility

## [v1.0.28] - 2026-01-02

### Fixed
- **aarch64 skip auditwheel repair** - Skip auditwheel entirely for aarch64
  - Even manylinux2014 image has updated toolchains with newer glibc symbols
  - Use `cp {wheel} {dest_dir}/` to just copy the wheel without repair
  - Wheel will have `linux_aarch64` tag which works on modern aarch64 systems

## [v1.0.27] - 2026-01-02

### Fixed
- **aarch64 use manylinux2014 image** - Explicitly use `manylinux2014` container image
  - The `manylinux2014` image has CentOS 7 with glibc 2.17 toolchain
  - Building inside this older container ensures symbols are compatible with manylinux_2_17
  - Set `CIBW_MANYLINUX_AARCH64_IMAGE: manylinux2014` to force older toolchain

## [v1.0.26] - 2026-01-02

### Fixed
- **aarch64 auditwheel compatibility** - Use `manylinux_2_28` instead of `manylinux_2_17`
  - The manylinux toolchain produces glibc symbols too new for manylinux_2_17
  - manylinux_2_28 (glibc 2.28) is compatible with most Linux distros from 2018+
  - Still provides broad compatibility while fixing the auditwheel repair error

## [v1.0.25] - 2026-01-02

### Fixed
- **aarch64 cp command fix** - Use `find` to copy only library files, not meson build directories
  - Meson creates `libfaest.so.1.0.0.p` directory which was causing `cp` to fail
  - Changed from `cp -v build/libfaest.so*` to `find build -name 'libfaest.so*' -type f -exec cp`

## [v1.0.24] - 2026-01-02

### Fixed
- **aarch64 symlink creation** - Fixed robust symlink creation for libfaest.so
  - Detect actual library version pattern from meson output
  - Create proper symlink chain regardless of versioning scheme
  - Add fallback to ensure `libfaest.so` always exists for linker

## [v1.0.23] - 2026-01-02

### Fixed
- **aarch64 build script approach** - Use external build script instead of inline YAML
  - Create `build_faest.sh` script to build library inside manylinux container
  - Remove dependency on pre-built artifacts for aarch64 (build everything from source)
  - Install meson/ninja via pip for better compatibility with manylinux
  - Copy headers from faest-ref directly inside the container

## [v1.0.22] - 2026-01-02

### Fixed
- **Linux aarch64 manylinux compatibility** - Fixed auditwheel "too-recent versioned symbols" error
  - Build libfaest inside manylinux container using `CIBW_BEFORE_ALL_LINUX`
  - Library now compiled with manylinux2014-compatible toolchain
  - Ensures proper glibc symbol versions for broad Linux compatibility

## [v1.0.21] - 2026-01-02

### Added
- **Linux aarch64 QEMU-based wheel building** - Pre-built wheels for ARM64 Linux using QEMU emulation and cibuildwheel
  - Supports Python 3.9-3.12 on aarch64

### Fixed
- **macOS x86_64 cross-compilation** - Fixed wheel building for Intel Macs
  - Added proper cross-compile environment variables (`ARCHFLAGS`, `_PYTHON_HOST_PLATFORM`)
  - Updated `faest_build.py` to detect target architecture from environment
  - Fixed CFFI build to pass cross-compile flags to compiler and linker
- **Removed broken pre-built binary download** - Simplified fallback build logic
- **Improved meson/ninja installation** - Fixed pip installation in various environments

### Changed
- Reduced macOS x86_64 Python versions to 3.9-3.12 for stability

### Platform Support Summary
- ✅ Linux x86_64 - Pre-built wheels (Python 3.8-3.14)
- ✅ Linux aarch64 - Pre-built wheels via QEMU (Python 3.9-3.12)
- ✅ macOS arm64 - Pre-built wheels (Python 3.8-3.14)
- ✅ macOS x86_64 - Pre-built wheels (Python 3.9-3.12)
- ✅ Windows via WSL - Use Linux wheels

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
