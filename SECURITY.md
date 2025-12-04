# Security Policy

## Supported Versions

PyFAEST is currently in active development. Security updates are provided for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue in PyFAEST, please report it responsibly.

### How to Report

**Please do not open a public GitHub issue for security vulnerabilities.**

Instead, report security issues via one of these methods:

1. **Email**: Send details to shreyas.sankpal@nyu.edu
2. **GitHub Security Advisory**: Use the [private vulnerability reporting feature](https://github.com/Shreyas582/pyfaest/security/advisories/new)

### What to Include

Please include the following information in your report:

- **Description** of the vulnerability
- **Steps to reproduce** the issue
- **Potential impact** and attack scenarios
- **Affected versions** of PyFAEST
- **Suggested fix** (if you have one)
- Your **contact information** for follow-up questions

### Response Timeline

- **Acknowledgment**: Within 48 hours
- **Initial assessment**: Within 7 days
- **Status updates**: Every 7-14 days until resolved
- **Fix release**: Depends on severity and complexity

### Security Considerations

⚠️ **Important Notes:**

PyFAEST is a Python binding to the FAEST reference implementation and inherits its security characteristics:

- **Reference Implementation**: FAEST is not yet optimized for production use
- **NIST Evaluation**: FAEST is a candidate scheme, not yet standardized
- **Side-Channel Attacks**: No protection against timing or power analysis attacks
- **Memory Safety**: Private keys are cleared from memory, but Python's memory management may leave traces
- **Cryptographic Vulnerabilities**: Report issues with FAEST itself to the [FAEST team](https://github.com/faest-sign/faest-ref/security)

### Scope

**In Scope:**
- Memory safety issues in Python bindings
- Input validation bypasses
- Incorrect API behavior leading to security issues
- Build system vulnerabilities
- Dependency vulnerabilities

**Out of Scope:**
- Issues in the underlying FAEST C library (report to upstream)
- Theoretical cryptographic attacks on FAEST
- General Python or OS-level security issues
- Performance-related issues (unless security-critical)

## Security Best Practices

When using PyFAEST:

1. **Keep Updated**: Use the latest version from PyPI
2. **Secure Storage**: Encrypt private keys at rest
3. **Secure Channels**: Transmit keys over secure channels only
4. **Key Lifecycle**: Properly destroy keys when no longer needed
5. **Randomness**: Ensure your system has a good entropy source
6. **Audit**: Review security-critical code paths in your application

## Disclosure Policy

- Security issues will be disclosed publicly after a fix is released
- Credit will be given to reporters who responsibly disclose vulnerabilities
- A security advisory will be published on GitHub for significant issues

## Academic Context

PyFAEST is developed as part of a Post-Quantum Cryptography course project at NYU. While we take security seriously, this is primarily an educational and research tool. For production use, please:

- Conduct your own security audit
- Consult with cryptography experts
- Follow industry best practices for key management
- Monitor NIST's PQC standardization process

## Contact

- **Security Issues**: shreyas.sankpal@nyu.edu
- **General Questions**: [GitHub Discussions](https://github.com/Shreyas582/pyfaest/discussions)
- **Bug Reports**: [GitHub Issues](https://github.com/Shreyas582/pyfaest/issues)

Thank you for helping keep PyFAEST secure!
