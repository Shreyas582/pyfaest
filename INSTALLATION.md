# PyFAEST Installation and Usage Guide

## Installation Methods

PyFAEST can be installed in two ways:
1. **From PyPI** (recommended for users) - includes bundled libraries
2. **From source** (for developers) - requires building FAEST C library

## Method 1: Install from PyPI (Recommended)

### Prerequisites

- **Linux** (x86_64 or aarch64/ARM64) or **macOS** (arm64 or x86_64) or **WSL on Windows**
- Python 3.8 or higher
- pip

### Installation

```bash
pip install pyfaest
```

That's it! The PyPI package includes pre-built wheels for:
- **Linux x86_64** (manylinux_2_17)
- **Linux aarch64 / ARM64** (Raspberry Pi, AWS Graviton, etc.)
- **macOS arm64** (Apple Silicon)
- **macOS x86_64** (Intel Macs)
- **Python 3.8, 3.9, 3.10, 3.11, 3.12, 3.13**

No compiler or build tools needed! For other platforms, PyPI will fall back to the source distribution with bundled libraries.

### Quick Test

```python
from faest import Keypair, sign, verify

keypair = Keypair.generate('128f')
message = b"Hello, FAEST!"
signature = sign(message, keypair.private_key)
assert verify(message, signature, keypair.public_key)
print("PyFAEST is working!")
```

---

## Method 2: Install from Source (Development)

This method is for developers who want to:
- Contribute to PyFAEST
- Use the latest development version
- Work with a custom FAEST library build
- Use unsupported platforms (macOS Intel, Linux aarch64)

### Prerequisites

- **Linux x86_64**, **ARM64**, or **macOS** (use WSL on Windows)
- Python 3.8 or higher
- FAEST C library (faest-ref) compiled
- Git

### Windows: Install WSL

Windows users must use WSL (Windows Subsystem for Linux):

```powershell
# In PowerShell as Administrator
wsl --install
# Restart your computer
```

### Step 1: Build FAEST C Library

First, ensure the FAEST reference implementation is compiled:

```bash
# Clone faest-ref if you haven't already
git clone https://github.com/faest-sign/faest-ref.git
cd faest-ref

# Build the library
meson setup build
meson compile -C build

# Verify the library was built
ls -la build/libfaest.so*
```

You should see `libfaest.so.1.0.0` and symlinks.

### Step 2: Set Up Python Environment

```bash
# Navigate to pyfaest directory (in WSL on Windows)
cd pyfaest

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Note:** Virtual environments avoid "externally managed environment" errors on modern Linux systems.

### Step 3: Update Bundled Libraries

Copy the FAEST library files to the pyfaest directory:

```bash
# From the pyfaest directory
FAEST_REF=../faest-ref bash scripts/update_libraries.sh
```

This copies:
- `libfaest.so.1.0.0` → `lib/linux/x86_64/`
- Header files → `include/`

### Step 4: Install PyFAEST

**Development mode (editable install - recommended for development):**
```bash
pip install -e .
```

**Regular installation:**
```bash
pip install .
```

The build process automatically:
1. Detects bundled libraries in `lib/linux/x86_64/`
2. Generates CFFI bindings
3. Sets runtime library paths (rpath) so no `LD_LIBRARY_PATH` is needed

### Step 5: Verify Installation

**Quick verification:**

```bash
python verify_install.py
```

Expected output:
```
============================================================
PyFAEST Verification Script
============================================================

1. Testing import... ✓ PASS
2. Testing key generation... ✓ PASS
3. Testing signing... ✓ PASS
4. Testing verification... ✓ PASS
5. Testing serialization... ✓ PASS

============================================================
✓ All tests passed (5/5)
PyFAEST is working correctly!
============================================================
```

**Run examples:**

```bash
# Basic usage
python examples/basic_usage.py

# Test all parameter sets
python examples/all_parameter_sets.py

# Key serialization patterns
python examples/key_serialization.py
```

**Run full test suite:**

```bash
# Run all 37 tests
pytest tests/ -v

# Run specific test class
pytest tests/test_pyfaest.py::TestKeyGeneration -v
```

---

## Troubleshooting

### Issue: "libfaest.so.1: cannot open shared object file"

**For PyPI installs:** This should not happen. If it does, please file a bug report.

**For source installs:**

**Cause:** Libraries not copied to `lib/linux/x86_64/` or runtime path not set correctly

**Solution:**
```bash
# Copy libraries using the update script
cd /path/to/pyfaest
FAEST_REF=/path/to/faest-ref bash scripts/update_libraries.sh

# Reinstall
pip install --force-reinstall -e .
```

### Issue: "cannot find -lfaest" during build

**Cause:** FAEST library not found in expected location

**Solution:**
```bash
# Verify library exists
ls -la lib/linux/x86_64/libfaest.so*

# If empty, run update script
FAEST_REF=/path/to/faest-ref bash scripts/update_libraries.sh

# Rebuild
pip install --force-reinstall -e .
```

### Issue: ImportError: _faest_cffi not found

**Cause:** CFFI bindings not built

**Solution:**
```bash
# Reinstall package
pip install --force-reinstall -e .

# Or manually build bindings
python faest_build.py
```

### Issue: "externally managed environment" error

**Cause:** Modern Linux distributions prevent system-wide pip installs

**Solution:** Use a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

### Issue: Test failures or import errors

**Solution:**
```bash
# Ensure you're in the virtual environment
source venv/bin/activate

# Verify library files exist
ls -la lib/linux/x86_64/

# Check if package is installed
pip list | grep pyfaest

# Reinstall clean
pip uninstall pyfaest
pip install -e .

# Run verification
python verify_install.py
```

### Issue: Windows build fails

**Cause:** Native Windows builds are not yet supported

**Solution:** Use WSL:
```powershell
# In PowerShell as Administrator
wsl --install
# Restart, then install in WSL environment
```

## Usage Examples

### Minimal Example

```python
from faest import Keypair, sign, verify

# Generate keys
keypair = Keypair.generate('128f')

# Sign
message = b"Hello, world!"
signature = sign(message, keypair.private_key)

# Verify
is_valid = verify(message, signature, keypair.public_key)
print(f"Valid: {is_valid}")  # True
```

### Save/Load Keys

```python
import json
import base64

# Save
key_data = {
    'param_set': keypair.param_set,
    'public_key': base64.b64encode(keypair.public_key.to_bytes()).decode(),
    'private_key': base64.b64encode(keypair.private_key.to_bytes()).decode()
}

with open('keypair.json', 'w') as f:
    json.dump(key_data, f)

# Load
with open('keypair.json', 'r') as f:
    data = json.load(f)

from faest import Keypair
keypair = Keypair.from_bytes(
    base64.b64decode(data['public_key']),
    base64.b64decode(data['private_key']),
    data['param_set']
)
```

## Architecture Overview

```
Your Python Script
       ↓
   faest/__init__.py (High-level API)
       ↓
   faest/core.py (Memory management, type conversion)
       ↓
   _faest_cffi.abi3.so (Generated by faest_build.py via CFFI)
       ↓
   libfaest.so.1 (FAEST C library in lib/linux/x86_64/)
```

### Build Process

1. **faest_build.py**: Defines CFFI bindings and generates `_faest_cffi` extension module
2. **setup.py**: Orchestrates the build via `cffi_modules`
3. **Runtime path**: `rpath` is set to find `libfaest.so.1` automatically
4. **Bundled libraries**: PyPI packages include pre-compiled libraries for each platform

## Parameter Set Selection Guide

| Use Case | Recommended |
|----------|-------------|
| General purpose | `128f` or `128s` |
| Maximum speed | `128f`, `192f`, or `256f` |
| Minimum signature size | `128s`, `192s`, or `256s` |
| High security (192-bit) | `192f` or `192s` |
| Maximum security (256-bit) | `256f` or `256s` |

## Next Steps

1. Run `python examples/basic_usage.py` to verify everything works
2. Read the examples in `examples/` directory
3. Check out the test suite in `tests/` for more usage patterns
4. Integrate into your project!

## Performance Tips

1. **Reuse keypairs** - Key generation is expensive
2. **Use the 'f' variants** for speed-critical applications
3. **Use the 's' variants** when bandwidth matters
4. **Precompute signatures** when possible

## Security Notes

⚠️ **Important:**
- This wraps the **reference implementation** - not optimized for production
- Private keys are automatically cleared from memory on deletion
- Always validate inputs before signing
- FAEST is still in NIST evaluation - not yet standardized

## Getting Help

- Check examples: `examples/`
- Read tests: `tests/test_pyfaest.py`

---

## Windows Native Support (Future / Experimental)

PyFAEST does not currently provide pre-built Windows native wheels. Windows users should use **WSL** (Windows Subsystem for Linux) which provides full Linux compatibility.

### Why No Windows Native Support?

1. **FAEST reference implementation** uses POSIX-specific features
2. **Build complexity** - Requires MSVC and Windows-specific patches
3. **Limited demand** - WSL provides excellent compatibility

### For Advanced Users: Building on Windows (Experimental)

If you need Windows native support, here's the general approach:

#### Option 1: Cross-compile from Linux (Recommended)

```bash
# Install MinGW-w64 cross-compiler on Linux
sudo apt-get install mingw-w64

# Create a meson cross-file
cat > win64-cross.txt << 'EOF'
[binaries]
c = 'x86_64-w64-mingw32-gcc'
cpp = 'x86_64-w64-mingw32-g++'
ar = 'x86_64-w64-mingw32-ar'
strip = 'x86_64-w64-mingw32-strip'
windres = 'x86_64-w64-mingw32-windres'

[host_machine]
system = 'windows'
cpu_family = 'x86_64'
cpu = 'x86_64'
endian = 'little'
EOF

# Build FAEST for Windows
cd faest-ref
meson setup build-win64 --cross-file=win64-cross.txt
meson compile -C build-win64
```

#### Option 2: Native MSVC Build (Requires Windows + Visual Studio)

```powershell
# Install prerequisites
# - Visual Studio 2019 or 2022 with C++ workload
# - Python 3.8+
# - Meson (pip install meson)
# - Ninja (pip install ninja)

# Set up environment (from VS Developer Command Prompt)
cd faest-ref
meson setup build
meson compile -C build

# Copy faest.dll to pyfaest\lib\windows\x64\
```

#### Known Issues with Windows Native

- Some FAEST code may use POSIX features requiring patches
- Windows DLL loading differs from Linux/macOS shared libraries  
- ABI compatibility between compilers can cause issues
- Testing coverage is limited

### Recommended: Use WSL

For Windows users, WSL provides the best experience:

```powershell
# Install WSL (PowerShell as Administrator)
wsl --install -d Ubuntu

# In WSL Ubuntu terminal
pip install pyfaest
python -c "from faest import Keypair; print('Success!')"
```

WSL2 provides:
- Full Linux compatibility
- Pre-built wheel support
- No build tools required
- Better performance than cross-compilation
- See API docs: `faest/core.py` has detailed docstrings
