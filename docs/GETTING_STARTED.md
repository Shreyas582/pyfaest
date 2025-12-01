# Getting Started with PyFAEST

Complete installation and usage guide for PyFAEST, the Python wrapper for the FAEST post-quantum signature scheme.

---

## Quick Start (5 Minutes)

### Installation

```bash
pip install pyfaest
```

### Verify Installation

```python
from faest import Keypair, sign, verify

# Generate keypair
keypair = Keypair.generate('128f')

# Sign a message
message = b"Hello, FAEST!"
signature = sign(message, keypair.private_key)

# Verify signature
assert verify(message, signature, keypair.public_key)
print("PyFAEST is working!")
```

---

## Installation Methods

### Method 1: From PyPI (Recommended)

**Prerequisites:**
- Linux (x86_64 or ARM64) or WSL on Windows
- Python 3.7+

**Install:**
```bash
pip install pyfaest
```

That's it! The package includes pre-compiled FAEST libraries.

### Method 2: From Source (Development)

**Prerequisites:**
- Linux or WSL on Windows
- Python 3.7+
- FAEST C library (faest-ref) compiled
- Git

**Steps:**

```bash
# 1. Build FAEST C library (if not already done)
git clone https://github.com/faest-sign/faest-ref.git
cd faest-ref
meson setup build
meson compile -C build

# 2. Navigate to pyfaest
cd /path/to/pyfaest

# 3. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Copy FAEST library files
FAEST_REF=/path/to/faest-ref bash scripts/update_libraries.sh

# 6. Install in development mode
pip install -e .

# 7. Verify
python verify_install.py
```

See [INSTALLATION.md](../INSTALLATION.md) for detailed instructions.

---

## Windows (WSL) Setup

### Why WSL?

Windows users must use WSL because:
- The FAEST C library is compiled for Linux
- Native Windows support is planned for future releases
- WSL provides full Linux compatibility

### Install WSL

```powershell
# In PowerShell as Administrator
wsl --install
# Restart your computer
```

### Access Windows Files from WSL

```bash
# Windows C:\ drive is mounted at /mnt/c/
cd /mnt/c/Projects/your-project
```

---

## Troubleshooting

### Error: "libfaest.so.1: cannot open shared object file"

**For PyPI installs:** This should not happen. File a bug report if it does.

**For source installs:**

```bash
# Ensure libraries are copied
FAEST_REF=/path/to/faest-ref bash scripts/update_libraries.sh

# Reinstall
pip install --force-reinstall -e .
```

### Error: "cannot find -lfaest" during build

**Solution:** Library files not in `lib/linux/x86_64/`:

```bash
# Verify library exists
ls -la lib/linux/x86_64/

# Copy libraries
FAEST_REF=/path/to/faest-ref bash scripts/update_libraries.sh

# Rebuild
pip install --force-reinstall -e .
```

### Error: "No module named '_faest_cffi'"

**Solution:** CFFI extension wasn't built:

```bash
pip install --force-reinstall -e .
```

### Error: "externally-managed-environment"

**Solution:** Use a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

---

## Basic Usage

### Generate Keys

```python
from faest import Keypair

# Generate keys for FAEST-128f
keypair = Keypair.generate('128f')

# Access keys
public_key = keypair.public_key
private_key = keypair.private_key

# Serialize keys
pub_bytes = public_key.to_bytes()
priv_bytes = private_key.to_bytes()
```

### Sign Messages

```python
from faest import sign

message = b"Important message"
signature = sign(message, private_key)

print(f"Signature size: {len(signature)} bytes")
# FAEST-128f signatures are 5924 bytes
```

### Verify Signatures

```python
from faest import verify

is_valid = verify(message, signature, public_key)

if is_valid:
    print("✓ Signature is valid")
else:
    print("✗ Signature is invalid")
```

### Available Parameter Sets

PyFAEST supports all 12 FAEST parameter sets:

```python
# Standard variants (AES-based)
'128f', '128s'  # NIST Level 1
'192f', '192s'  # NIST Level 3  
'256f', '256s'  # NIST Level 5

# EM variants (Extended Mode)
'em_128f', 'em_128s'
'em_192f', 'em_192s'
'em_256f', 'em_256s'
```

**Trade-offs:**
- `f` variants: Faster signing and verification, larger signatures
- `s` variants: Smaller signatures, slower operations
- EM variants: Extended mode with different security assumptions

### Security Levels

| Parameter | NIST Level | Public Key | Private Key | Signature Size |
|-----------|------------|------------|-------------|----------------|
| 128f/s    | 1          | 32 bytes   | 32 bytes    | 5924 / 4506 B  |
| 192f/s    | 3          | 48 bytes   | 40 bytes    | 14948 / 11260 B|
| 256f/s    | 5          | 48 bytes   | 48 bytes    | 26548 / 20696 B|
| em_256f/s | 5          | 64 bytes   | 64 bytes    | 23476 / 17984 B|

---

## Testing

```bash
# Verify installation
python verify_install.py

# Run all tests (37 tests)
pytest tests/ -v

# Run specific test class
pytest tests/test_pyfaest.py::TestKeyGeneration -v
```

---

## Examples

Check the `examples/` directory:

```bash
# Basic usage
python examples/basic_usage.py

# All parameter sets
python examples/all_parameter_sets.py

# Key serialization
python examples/key_serialization.py
```

---

## Next Steps

- **API Reference:** See [README.md](../README.md) for complete API documentation
- **Installation Details:** Check [INSTALLATION.md](../INSTALLATION.md) for troubleshooting
- **Development:** Read [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) for contributing
- **Publishing:** See [MAINTAINER_GUIDE.md](MAINTAINER_GUIDE.md) for release process

---

## Support

- **GitHub Issues:** https://github.com/Shreyas582/pyfaest/issues
- **FAEST Website:** https://faest.info/
- **NIST PQC Project:** https://csrc.nist.gov/projects/post-quantum-cryptography
