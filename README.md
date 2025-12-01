# PyFAEST - Python Bindings for FAEST

[![PyPI version](https://badge.fury.io/py/pyfaest.svg)](https://badge.fury.io/py/pyfaest)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Python wrapper for the FAEST (Fast AES-based Signature with Tight security) post-quantum digital signature scheme.

## Overview

FAEST is a post-quantum signature scheme submitted to the NIST PQC standardization process. This Python package provides high-level bindings to the C reference implementation:

- 🔐 **Quantum-resistant signatures** based on symmetric cryptography
- 🚀 **High performance** - Direct binding to optimized C code via CFFI
- 🛡️ **Memory-safe** - Automatic private key clearing
- 🎯 **Pythonic API** - Clean, intuitive interface
- 📦 **12 parameter sets** - All FAEST variants supported

## Installation

### From PyPI (Recommended)

```bash
pip install pyfaest
```

### From Source

```bash
git clone https://github.com/Shreyas582/pyfaest.git
cd pyfaest
pip install -e .
```

**Note:** Currently supports Linux only. Windows users should use WSL.

## Quick Start

```python
from faest import Keypair, sign, verify

# Generate a keypair
keypair = Keypair.generate('128f')

# Sign a message
message = b"Hello, quantum-resistant world!"
signature = sign(message, keypair.private_key)

# Verify the signature
is_valid = verify(message, signature, keypair.public_key)
print(f"Valid: {is_valid}")  # True
```

## Parameter Sets

PyFAEST supports all 12 FAEST parameter sets:

| Parameter Set | Security Level | Public Key | Private Key | Signature  |
|--------------|----------------|------------|-------------|------------|
| `128f`       | NIST Level 1  | 32 bytes   | 32 bytes    | 5,924 B    |
| `128s`       | NIST Level 1  | 32 bytes   | 32 bytes    | 4,506 B    |
| `192f`       | NIST Level 3  | 48 bytes   | 40 bytes    | 14,948 B   |
| `192s`       | NIST Level 3  | 48 bytes   | 40 bytes    | 11,260 B   |
| `256f`       | NIST Level 5  | 48 bytes   | 48 bytes    | 26,548 B   |
| `256s`       | NIST Level 5  | 48 bytes   | 48 bytes    | 20,696 B   |
| `em_128f`    | NIST Level 1  | 32 bytes   | 32 bytes    | 5,060 B    |
| `em_128s`    | NIST Level 1  | 32 bytes   | 32 bytes    | 3,906 B    |
| `em_192f`    | NIST Level 3  | 48 bytes   | 48 bytes    | 12,380 B   |
| `em_192s`    | NIST Level 3  | 48 bytes   | 48 bytes    | 9,340 B    |
| `em_256f`    | NIST Level 5  | 64 bytes   | 64 bytes    | 23,476 B   |
| `em_256s`    | NIST Level 5  | 64 bytes   | 64 bytes    | 17,984 B   |

**Suffix meanings:**
- `f` = Fast (optimized for speed)
- `s` = Small (optimized for signature size)  
- `em_*` = Extended mode variants

**Note:** 192-bit variants have asymmetric key sizes (private=40, public=48) by design.

## API Reference

### Key Generation

```python
from faest import Keypair

# Generate a new keypair
keypair = Keypair.generate('128f')

# Access individual keys
public_key = keypair.public_key
private_key = keypair.private_key
param_set = keypair.param_set

# Validate keypair
is_valid = keypair.validate()
```

### Signing and Verification

```python
from faest import sign, verify

# Sign a message
signature = sign(message, private_key)

# Verify a signature  
is_valid = verify(message, signature, public_key)
```

### Key Serialization

```python
# Export keys as bytes
pk_bytes = public_key.to_bytes()
sk_bytes = private_key.to_bytes()

# Import from bytes
keypair = Keypair.from_bytes(pk_bytes, sk_bytes, '128f')

# Or create keys individually
from faest import PublicKey, PrivateKey
public_key = PublicKey(pk_bytes, '128f')
private_key = PrivateKey(sk_bytes, '128f')
```

### Error Handling

```python
from faest import (
    FaestError,           # Base exception
    KeyGenerationError,   # Key generation failed
    SignatureError,       # Signing failed
    VerificationError,    # Verification failed
    InvalidKeyPairError,  # Keypair validation failed
)

try:
    keypair = Keypair.generate('128f')
    signature = sign(message, keypair.private_key)
except KeyGenerationError as e:
    print(f"Key generation failed: {e}")
except SignatureError as e:
    print(f"Signing failed: {e}")
```

## Examples

Complete examples in the `examples/` directory:

- **`basic_usage.py`** - Simple signing and verification
- **`all_parameter_sets.py`** - Testing all 12 parameter sets
- **`key_serialization.py`** - Key import/export patterns

## Documentation

- **[Installation Guide](INSTALLATION.md)** - Detailed installation instructions
- **[Getting Started](docs/GETTING_STARTED.md)** - Quick start tutorial
- **[Developer Guide](docs/DEVELOPER_GUIDE.md)** - Architecture and internals
- **[Maintainer Guide](docs/MAINTAINER_GUIDE.md)** - Release and publishing

## Requirements

- Python 3.7 or higher
- Linux (WSL for Windows users)
- CFFI >= 1.15.0 (automatically installed)

## Security Considerations

⚠️ **Important Security Notes:**

- **Reference implementation** - Not yet optimized for production
- **NIST evaluation** - FAEST is a candidate, not yet standardized
- **Memory safety** - Private keys automatically cleared from memory
- **Side channels** - No protection against timing/power analysis attacks
- **Secure storage** - Store private keys encrypted at rest

## Performance

Typical performance on modern hardware (single core):

| Operation        | 128f  | 128s  | 256f  | 256s  |
|-----------------|-------|-------|-------|-------|
| Key generation  | ~1 ms | ~1 ms | ~2 ms | ~2 ms |
| Signing         | ~5 ms | ~8 ms | ~15ms | ~25ms |
| Verification    | ~5 ms | ~8 ms | ~15ms | ~25ms |

`f` variants are faster, `s` variants produce smaller signatures.

## Platform Support

| Platform        | Status      | Notes                    |
|----------------|-------------|--------------------------|
| Linux x86_64   | ✅ Supported | Primary platform         |
| Linux aarch64  | ✅ Supported | ARM support              |
| macOS x86_64   | 🚧 Planned  | Coming soon              |
| macOS ARM64    | 🚧 Planned  | Coming soon              |
| Windows (WSL)  | ✅ Supported | Use WSL for now          |
| Windows native | 🚧 Planned  | Future release           |

## Development

### Running Tests

```bash
pip install pytest
pytest tests/ -v
```

### Building from Source

See [INSTALLATION.md](INSTALLATION.md) for detailed instructions.

**Quick version:**

```bash
# Build FAEST C library first
git clone https://github.com/faest-sign/faest-ref.git
cd faest-ref
meson setup build
meson compile -C build

# Install PyFAEST
cd /path/to/pyfaest
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Copy library files
FAEST_REF=/path/to/faest-ref bash scripts/update_libraries.sh

# Install in development mode
pip install -e .

# Verify
python verify_install.py
```

### Project Structure

```
pyfaest/
├── faest/              # Python package
│   ├── __init__.py     # Public API exports
│   └── core.py         # Main implementation (550+ lines)
├── lib/                # Bundled FAEST libraries
├── include/            # C header files  
├── examples/           # Usage examples
├── tests/              # Test suite (37 tests)
├── docs/               # Documentation
├── scripts/            # Build/release scripts
├── faest_build.py      # CFFI build script
└── setup.py            # Package configuration
```

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

See [DEVELOPER_GUIDE.md](docs/DEVELOPER_GUIDE.md) for more details.

## Citation

If you use PyFAEST in research, please cite:

```bibtex
@software{pyfaest,
  title = {PyFAEST: Python Bindings for FAEST},
  author = {PyFAEST Contributors},
  year = {2025},
  url = {https://github.com/Shreyas582/pyfaest}
}
```

## References

- [FAEST Official Website](https://faest.info/)
- [FAEST Specification](https://faest.info/faest-spec-v2.0.pdf)
- [NIST PQC Project](https://csrc.nist.gov/projects/post-quantum-cryptography)
- [faest-ref GitHub](https://github.com/faest-sign/faest-ref)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## Support

- **Issues**: [GitHub Issues](https://github.com/Shreyas582/pyfaest/issues)
- **Documentation**: [docs/](docs/)
- **Examples**: [examples/](examples/)

## Acknowledgments

PyFAEST is built on top of the FAEST reference implementation by the FAEST team. Special thanks to all contributors to the FAEST project.

## NOTE from Author
I have created this for a Post-Quantum Cryptography class project at NYU.