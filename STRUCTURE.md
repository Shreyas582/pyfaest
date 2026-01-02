# PyFAEST Project Structure

This document describes the organization of the PyFAEST project, following Python packaging best practices.

---

## Directory Structure

```
pyfaest/
├── faest/                      # Main Python package
│   ├── __init__.py            # Package initialization
│   └── core.py                # Core implementation (550+ lines)
│
├── docs/                       # Documentation (consolidated)
│   ├── README.md              # Documentation index
│   ├── GETTING_STARTED.md     # Installation & usage guide (users)
│   ├── DEVELOPER_GUIDE.md     # Architecture & contributing (developers)
│   └── MAINTAINER_GUIDE.md    # Publishing & releases (maintainers)
│
├── examples/                   # Usage examples
│   ├── basic_usage.py         # Simple signing/verification
│   ├── all_parameter_sets.py  # Test all 12 parameter sets
│   └── key_serialization.py   # Key import/export examples
│
├── tests/                      # Test suite
│   └── test_core.py           # 37 tests covering all functionality
│
├── scripts/                    # Helper scripts
│   ├── prepare_release.sh     # Bundle libraries for PyPI
│   └── update_libraries.sh    # Update from faest-ref
│
├── lib/                        # Bundled FAEST libraries (PyPI)
│   └── linux/
│       └── x86_64/
│           └── libfaest.so.1.0.0  # Compiled library (958KB)
│
├── include/                    # C header files (34 files)
│   ├── faest_*.h              # Generated parameter headers
│   ├── faest_defines.h        # Core definitions
│   └── ...                    # Supporting headers
│
├── README.md                   # Main documentation + API reference
├── CHANGELOG.md                # Version history
├── LICENSE                     # MIT License
├── .gitignore                  # Git exclusions
│
├── setup.py                    # Package configuration
├── pyproject.toml              # Modern Python packaging
├── setup.cfg                   # Setuptools configuration
├── MANIFEST.in                 # Distribution file inclusions
│
├── faest_build.py              # CFFI builder (platform detection)
├── requirements.txt            # Python dependencies
│
├── quickstart.py               # Quick demo script
└── verify_install.py           # Installation verification
```

---

## Entry Points for Different Users

### New Users
1. Start with root `README.md` - API overview
2. Then `docs/GETTING_STARTED.md` - Installation
3. Try `quickstart.py` or `examples/basic_usage.py`

### Developers
1. `docs/DEVELOPER_GUIDE.md` - Architecture
2. `faest/core.py` - Implementation
3. `tests/test_core.py` - Test examples

### Maintainers
1. `docs/MAINTAINER_GUIDE.md` - Release process
2. `scripts/` - Helper scripts
3. `CHANGELOG.md` - Version tracking

---

## Compliance Checklist

- [x] **PEP 517/518:** `pyproject.toml` with build system
- [x] **PEP 621:** Project metadata in `pyproject.toml`
- [x] **PEP 440:** Semantic versioning (X.Y.Z)
- [x] **Setuptools:** Proper `setup.py` and `setup.cfg`
- [x] **MANIFEST.in:** Includes all necessary files
- [x] **LICENSE:** MIT license included
- [x] **README.md:** Comprehensive documentation
- [x] **CHANGELOG.md:** Version history tracking
- [x] **.gitignore:** Excludes build artifacts
- [x] **Type hints:** Used in `faest/core.py`
- [x] **Docstrings:** All public functions documented
- [x] **Tests:** 37 tests with pytest
- [x] **Examples:** Clear usage demonstrations

---

## Future Improvements

### Multi-Platform Libraries
- [ ] Add `lib/macos/x86_64/` and `lib/macos/arm64/`
- [ ] Add `lib/windows/x64/`
- [ ] Update `faest_build.py` for platform detection

### CI/CD
- [ ] GitHub Actions for automated testing
- [ ] Automated PyPI publishing on tag
- [ ] Multi-platform builds

### Documentation
- [ ] Add type stubs (.pyi files)
- [ ] Sphinx documentation generation
- [ ] ReadTheDocs integration

---

## Maintenance

### When FAEST Updates

1. Update faest-ref: `cd ../faest-ref && git pull`
2. Rebuild: `meson compile -C build`
3. Update libraries: `bash scripts/update_libraries.sh`
4. Bump version in `setup.py` and `pyproject.toml`
5. Update `CHANGELOG.md`
6. Test: `pytest tests/ -v`
7. Build: `python -m build`
8. Publish: `twine upload dist/*`

### Adding New Features

1. Implement in `faest/core.py`
2. Add tests in `tests/test_core.py`
3. Update `README.md` API reference
4. Add example to `examples/` if needed
5. Update `CHANGELOG.md`

