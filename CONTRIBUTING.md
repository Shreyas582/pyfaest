# Contributing to PyFAEST

Thank you for your interest in contributing to PyFAEST! This document provides guidelines for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Signing Your Commits](#signing-your-commits)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Create a branch** for your changes
4. **Make your changes** with tests
5. **Submit a pull request**

## How to Contribute

### Types of Contributions

We welcome many types of contributions:

- 🐛 **Bug fixes** - Fix issues in existing code
- ✨ **New features** - Add new functionality
- 📝 **Documentation** - Improve docs, examples, or comments
- 🧪 **Tests** - Add or improve test coverage
- 🎨 **Code quality** - Refactoring, type hints, performance
- 🔧 **Build/CI** - Improve build system or workflows
- 🌍 **Platform support** - Add support for new platforms

### Before You Start

- Check [existing issues](https://github.com/Shreyas582/pyfaest/issues) to avoid duplicate work
- For major changes, open an issue first to discuss the approach
- For small fixes, feel free to open a PR directly

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- C compiler (gcc/clang) for building FAEST library
- meson and ninja build tools

### Setup Instructions

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/pyfaest.git
cd pyfaest

# Add upstream remote
git remote add upstream https://github.com/Shreyas582/pyfaest.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install pytest pytest-cov

# Build FAEST C library
git clone https://github.com/faest-sign/faest-ref.git
cd faest-ref
meson setup build
meson compile -C build
cd ..

# Copy libraries
export FAEST_REF=./faest-ref
bash scripts/update_libraries.sh

# Install in development mode
pip install -e .

# Verify installation
python verify_install.py
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=faest --cov-report=html

# Run specific test
pytest tests/test_pyfaest.py::test_key_generation -v
```

## Coding Standards

### Python Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable and function names
- Add docstrings to public functions and classes
- Keep functions focused and reasonably sized
- Use type hints where appropriate

### Code Structure

```python
def sign(message: bytes, private_key: PrivateKey) -> bytes:
    """
    Sign a message using FAEST.
    
    Args:
        message: The message to sign
        private_key: The private key for signing
        
    Returns:
        The signature bytes
        
    Raises:
        SignatureError: If signing fails
    """
    # Implementation
```

### Documentation

- Update README.md for user-facing changes
- Update docstrings for API changes
- Add examples for new features
- Update CHANGELOG.md following [Keep a Changelog](https://keepachangelog.com/)

## Testing

### Writing Tests

- Add tests for all new functionality
- Ensure tests are deterministic and isolated
- Use descriptive test names
- Test both success and failure cases

```python
def test_sign_with_invalid_key():
    """Test that signing with invalid key raises appropriate error."""
    with pytest.raises(SignatureError):
        sign(b"message", invalid_key)
```

### Test Coverage

- Maintain or improve existing coverage
- Aim for >90% coverage for new code
- Critical paths should have 100% coverage

## Signing Your Commits

**All commits to the main branch must be GPG signed.** This ensures commit authenticity and prevents impersonation.

### Why Sign Commits?

- ✅ Verifies you are the actual author
- ✅ Prevents unauthorized commits in your name
- ✅ Industry best practice for security projects
- ✅ Shows a "Verified" badge on GitHub

### Setup Instructions

#### 1. Generate a GPG Key

```bash
# Generate key
gpg --full-generate-key

# When prompted:
# - Choose: (1) RSA and RSA
# - Key size: 4096
# - Expiration: 0 (no expiration) or set as desired
# - Enter your name and email (must match your GitHub email)
```

#### 2. Get Your Key ID

```bash
# List your keys
gpg --list-secret-keys --keyid-format=long

# Output looks like:
# sec   rsa4096/ABCD1234EFGH5678 2025-12-03
#       Your key ID is: ABCD1234EFGH5678

# Export your public key
gpg --armor --export ABCD1234EFGH5678
```

#### 3. Add Key to GitHub

1. Copy the entire output from the export command (including `-----BEGIN PGP PUBLIC KEY BLOCK-----` and `-----END PGP PUBLIC KEY BLOCK-----`)
2. Go to [GitHub Settings → SSH and GPG keys](https://github.com/settings/keys)
3. Click **New GPG key**
4. Paste your public key
5. Click **Add GPG key**

#### 4. Configure Git

```bash
# Set your signing key (replace with YOUR key ID)
git config --global user.signingkey ABCD1234EFGH5678

# Enable automatic signing for all commits
git config --global commit.gpgsign true

# Enable automatic signing for all tags
git config --global tag.gpgsign true

# Verify your email matches GitHub
git config --global user.email "your.email@example.com"
```

#### 5. For Windows Users

```powershell
# Tell Git where to find GPG
git config --global gpg.program "C:\Program Files (x86)\GnuPG\bin\gpg.exe"

# Or if using GPG4Win:
git config --global gpg.program "C:\Program Files (x86)\GnuPG\bin\gpg.exe"
```

### Verify It Works

```bash
# Make a test commit
git commit --allow-empty -m "Test signed commit"

# Verify the signature
git log --show-signature -1

# You should see "gpg: Good signature from..."
```

### Troubleshooting

**"gpg: signing failed: Inappropriate ioctl for device"** (Linux/macOS):
```bash
export GPG_TTY=$(tty)
echo 'export GPG_TTY=$(tty)' >> ~/.bashrc  # or ~/.zshrc
```

**"gpg: signing failed: No secret key"**:
```bash
# Check your key is listed
gpg --list-secret-keys

# Verify git config
git config --global user.signingkey
```

**Commit rejected: "Commit signature verification failed"**:
- Ensure your GPG key is added to GitHub
- Verify your git email matches the key email
- Check that your key hasn't expired

### Additional Resources

- [GitHub's GPG Documentation](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification)
- [Git Tools - Signing Your Work](https://git-scm.com/book/en/v2/Git-Tools-Signing-Your-Work)

## Pull Request Process

### Before Submitting

1. **Update your fork** with latest upstream changes:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Ensure commits are signed**:
   ```bash
   # Check if your commits are signed
   git log --show-signature -1
   
   # If not signed, configure GPG (see "Signing Your Commits" section above)
   ```

3. **Run tests** and ensure they pass:
   ```bash
   pytest tests/ -v
   ```

4. **Update documentation** if needed

5. **Update CHANGELOG.md** under `[Unreleased]` section

### PR Guidelines

- **Title**: Clear, descriptive title (e.g., "Fix memory leak in key generation")
- **Description**: Explain what and why, not just how
- **Link issues**: Reference related issues (e.g., "Fixes #123")
- **Keep it focused**: One feature/fix per PR
- **Clean history**: Squash minor commits if needed

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
How was this tested?

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] All tests pass
- [ ] Commits are signed (GPG)
```

### Review Process

- Maintainers will review your PR
- Address feedback and requested changes
- Once approved, your PR will be merged
- Your contribution will be credited in releases

## Reporting Bugs

### Before Reporting

- Check [existing issues](https://github.com/Shreyas582/pyfaest/issues)
- Verify the bug exists in the latest version
- Try to reproduce with a minimal example

### Bug Report Template

```markdown
**Describe the bug**
Clear description of what the bug is

**To Reproduce**
Steps to reproduce:
1. Import pyfaest
2. Call function X with Y
3. See error

**Expected behavior**
What you expected to happen

**Actual behavior**
What actually happened

**Environment:**
- OS: [e.g., Ubuntu 22.04]
- Python version: [e.g., 3.11]
- PyFAEST version: [e.g., 1.0.15]

**Additional context**
Any other relevant information
```

## Suggesting Enhancements

### Feature Requests

- Open a [GitHub Discussion](https://github.com/Shreyas582/pyfaest/discussions) first
- Describe the use case and benefits
- Consider implementation complexity
- Be open to feedback and alternatives

### Enhancement Template

```markdown
**Is your feature request related to a problem?**
Description of the problem

**Describe the solution you'd like**
What you want to happen

**Describe alternatives you've considered**
Other approaches you've thought about

**Additional context**
Any other relevant information
```

## Project Structure

```
pyfaest/
├── faest/              # Python package
│   ├── __init__.py     # Public API
│   └── core.py         # Core implementation
├── lib/                # Bundled libraries
├── include/            # C headers
├── tests/              # Test suite
├── examples/           # Usage examples
├── docs/               # Documentation
├── scripts/            # Build scripts
├── faest_build.py      # CFFI builder
└── setup.py            # Package setup
```

## Release Process

For maintainers:

1. Update version in `setup.py` and `pyproject.toml`
2. Update `CHANGELOG.md` with release notes
3. Create and push tag: `git tag -a v1.0.x -m "Release v1.0.x"`
4. Create GitHub release
5. CI automatically publishes to PyPI

## Community

- **Discussions**: Ask questions, share ideas
- **Issues**: Report bugs, request features  
- **Pull Requests**: Submit contributions
- **Email**: shreyas.sankpal@nyu.edu for security issues

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be:
- Listed in release notes
- Credited in the repository
- Appreciated by the community!

Thank you for contributing to PyFAEST! 🎉
