# PyFAEST Publishing and Maintenance Guide

Complete guide for maintainers on preparing releases and publishing PyFAEST to PyPI.

---

## Publishing Strategy

PyFAEST bundles compiled FAEST libraries for a simple installation experience. Users can `pip install pyfaest` without needing to compile the C library themselves.

### Benefits

✅ Simple installation: Works out of the box  
✅ No external dependencies required  
✅ Cross-platform support (Linux, macOS, Windows planned)  
✅ Version control: Each PyFAEST release matches a specific FAEST version  
✅ License compliance: FAEST license included  

---

## Release Workflow

### 1. Update FAEST Library (if needed)

When a new FAEST version is released:

```bash
# Update FAEST repository
cd /path/to/faest-ref
git pull

# Rebuild library
meson compile -C build

# Copy updated libraries to PyFAEST
cd /path/to/pyfaest
FAEST_REF=/path/to/faest-ref bash scripts/update_libraries.sh
```

The script copies:
- `libfaest.so.1.0.0` → `lib/linux/x86_64/`
- All header files → `include/`
- Creates version tracking in `FAEST_VERSION.txt`

### 2. Version Management

**Semantic Versioning:**
```
PyFAEST Version = X.Y.Z

X (Major): Breaking API changes
Y (Minor): New FAEST versions, new features  
Z (Patch): Bug fixes, documentation updates
```

**Examples:**
- `1.0.0` - Initial release (FAEST v2.0.4)
- `1.1.0` - Updated to FAEST v2.0.5
- `1.1.1` - Bug fix in Python wrapper
- `2.0.0` - Breaking API changes

**Update version in:**

1. `setup.py`:
   ```python
   version='1.1.0',
   ```

2. `pyproject.toml`:
   ```toml
   version = "1.1.0"
   ```

3. `FAEST_VERSION.txt`:
   ```
   2.0.5
   ```

### 3. Update Changelog

Edit `CHANGELOG.md`:

```markdown
## [1.1.0] - 2025-11-25

### Changed
- Updated to FAEST library v2.0.5

### Added
- Support for new parameter set

### Fixed
- Bug in signature verification
- Memory leak in key generation
```

---

## Pre-Release Checklist

### Code Quality

- [ ] All tests pass: `pytest tests/ -v`
- [ ] No linting errors: `pylint faest/`
- [ ] Documentation is up to date
- [ ] Examples all work correctly

### Bundle Libraries

- [ ] Run preparation script: `bash scripts/prepare_release.sh`
- [ ] Verify bundled files:
  ```bash
  ls -lh lib/linux/x86_64/libfaest.so*
  ls include/*.h | wc -l  # Should be 34+ files
  ```

### Version Updates

- [ ] Updated `setup.py` version
- [ ] Updated `pyproject.toml` version  
- [ ] Updated `CHANGELOG.md`
- [ ] Updated `FAEST_VERSION.txt`

### Testing

- [ ] Clean build directory:
  ```bash
  rm -rf build/ dist/ *.egg-info
  ```

- [ ] Build distribution:
  ```bash
  python -m build
  ```

- [ ] Check distribution contents:
  ```bash
  tar -tzf dist/pyfaest-*.tar.gz | grep -E '(lib/|include/)'
  ```

- [ ] Test in clean environment:
  ```bash
  python3 -m venv test_env
  source test_env/bin/activate
  pip install dist/pyfaest-*.tar.gz
  python -c "from faest import Keypair; Keypair.generate('128f')"
  deactivate
  rm -rf test_env
  ```

---

## Publishing to PyPI

### TestPyPI (Recommended First)

Test the release process without affecting production:

```bash
# Install twine
pip install twine

# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test installation
python3 -m venv testpypi_env
source testpypi_env/bin/activate
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple pyfaest
python -c "from faest import Keypair; print('TestPyPI works!')"
deactivate
rm -rf testpypi_env
```

**TestPyPI Account:** https://test.pypi.org/account/register/

### Production PyPI

After successful TestPyPI verification:

```bash
# Upload to production PyPI
twine upload dist/*

# Verify on PyPI
# https://pypi.org/project/pyfaest/

# Test installation
python3 -m venv prod_test
source prod_test/bin/activate
pip install pyfaest
python -c "from faest import Keypair; print('Production works!')"
deactivate
rm -rf prod_test
```

**PyPI Account:** https://pypi.org/account/register/

### Using API Tokens (Recommended)

Instead of passwords, use API tokens for authentication:

1. Generate token on PyPI: Account Settings → API tokens
2. Save to `~/.pypirc`:
   ```ini
   [pypi]
   username = __token__
   password = pypi-AgEIcHlwaS5vcmc...

   [testpypi]
   username = __token__
   password = pypi-AgENdGVzdC5weXBpLm9yZw...
   ```

---

## Post-Release Tasks

### GitHub Release

- [ ] Create Git tag:
  ```bash
  git tag -a v1.1.0 -m "Release version 1.1.0"
  git push origin v1.1.0
  ```

- [ ] Create GitHub release with:
  - Tag: `v1.1.0`
  - Title: `PyFAEST v1.1.0`
  - Description: Copy from CHANGELOG.md
  - Attach distribution files: `dist/pyfaest-1.1.0.tar.gz`

### Verification

- [ ] Verify PyPI page looks correct
- [ ] Test installation on fresh system
- [ ] Update documentation links if needed
- [ ] Announce release (Twitter, mailing list, etc.)

---

## Multi-Platform Support (Future)

Currently, PyFAEST includes Linux x86_64 libraries. For full cross-platform support:

### Linux

```bash
# x86_64 (already supported)
meson compile -C build
cp build/libfaest.so.1.0.0 pyfaest/lib/linux/x86_64/

# aarch64 (ARM64)
# Requires ARM64 build machine or cross-compilation
```

### macOS

```bash
# x86_64 and arm64 (universal binary)
meson compile -C build
cp build/libfaest.dylib pyfaest/lib/macos/
```

### Windows

```bash
# Native Windows build (requires MinGW or similar)
# Or cross-compile from Linux
```

Update `faest_build.py` to detect and load the correct library for each platform.

---

## Troubleshooting

### Build Errors

**Issue:** `error: unable to create file lib/...`

**Solution:** Run `scripts/prepare_release.sh` to create library directories

### Upload Errors

**Issue:** `HTTPError: 403 Forbidden`

**Solution:** Check credentials in `~/.pypirc`, regenerate API token if needed

### Installation Failures

**Issue:** `ModuleNotFoundError: No module named '_faest_cffi'`

**Solution:** Ensure `faest_build.py` runs during `pip install`, check build logs

---

## Support

- **PyPI Project:** https://pypi.org/project/pyfaest/
- **GitHub Issues:** https://github.com/Shreyas582/pyfaest/issues
- **Contact:** shreyas.sankpal@nyu.edu
