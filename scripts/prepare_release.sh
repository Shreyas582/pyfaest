#!/bin/bash
# Prepare PyFAEST for release by bundling libraries and headers
# Run this before building distributions for PyPI

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYFAEST_DIR="$(dirname "$SCRIPT_DIR")"
FAEST_REF="${FAEST_REF:-$(dirname "$PYFAEST_DIR")}"

echo "============================================================"
echo "Preparing PyFAEST Release"
echo "============================================================"
echo ""
echo "PyFAEST directory: $PYFAEST_DIR"
echo "FAEST-ref directory: $FAEST_REF"
echo ""

# Validate FAEST directory
if [ ! -d "$FAEST_REF/build" ]; then
    echo "ERROR: FAEST build directory not found at $FAEST_REF/build"
    echo ""
    echo "Please build FAEST first:"
    echo "  cd $FAEST_REF"
    echo "  meson setup build"
    echo "  meson compile -C build"
    echo ""
    echo "Or set FAEST_REF environment variable:"
    echo "  export FAEST_REF=/path/to/faest-ref"
    exit 1
fi

# Create directories
echo "Creating directory structure..."
mkdir -p "$PYFAEST_DIR/lib/linux/x86_64"
mkdir -p "$PYFAEST_DIR/lib/linux/aarch64"
mkdir -p "$PYFAEST_DIR/lib/macos/x86_64"
mkdir -p "$PYFAEST_DIR/lib/macos/arm64"
mkdir -p "$PYFAEST_DIR/lib/windows/x64"
mkdir -p "$PYFAEST_DIR/include"

# Copy Linux library (current build)
echo ""
echo "Copying Linux x86_64 library..."
if [ -f "$FAEST_REF/build/libfaest.so.1.0.0" ]; then
    cp "$FAEST_REF/build/libfaest.so.1.0.0" "$PYFAEST_DIR/lib/linux/x86_64/"
    cd "$PYFAEST_DIR/lib/linux/x86_64"
    ln -sf libfaest.so.1.0.0 libfaest.so.1
    ln -sf libfaest.so.1 libfaest.so
    cd - > /dev/null
    echo "  ✓ Copied $(ls -lh "$PYFAEST_DIR/lib/linux/x86_64/libfaest.so.1.0.0" | awk '{print $5}')"
else
    echo "  ⚠ Warning: libfaest.so.1.0.0 not found in $FAEST_REF/build"
fi

# Copy headers
echo ""
echo "Copying headers..."
cp "$FAEST_REF/build"/*.h "$PYFAEST_DIR/include/" 2>/dev/null || true
cp "$FAEST_REF"/*.h "$PYFAEST_DIR/include/" 2>/dev/null || true
HEADER_COUNT=$(ls "$PYFAEST_DIR/include"/*.h 2>/dev/null | wc -l)
echo "  ✓ Copied $HEADER_COUNT header files"

# Get FAEST version
echo ""
echo "Recording FAEST version..."
cd "$FAEST_REF"
if git rev-parse --git-dir > /dev/null 2>&1; then
    FAEST_VERSION=$(git describe --tags 2>/dev/null || git rev-parse --short HEAD)
    FAEST_COMMIT=$(git rev-parse HEAD)
    echo "FAEST_VERSION=$FAEST_VERSION" > "$PYFAEST_DIR/FAEST_VERSION.txt"
    echo "FAEST_COMMIT=$FAEST_COMMIT" >> "$PYFAEST_DIR/FAEST_VERSION.txt"
    echo "BUNDLED_DATE=$(date -u +%Y-%m-%d)" >> "$PYFAEST_DIR/FAEST_VERSION.txt"
    echo "  ✓ FAEST version: $FAEST_VERSION"
else
    echo "  ⚠ Warning: Not a git repository, version info not recorded"
fi

cd "$PYFAEST_DIR"

# Create/update CHANGELOG entry
echo ""
echo "Update CHANGELOG.md with:"
echo ""
echo "## [Unreleased]"
echo "- Bundled FAEST library version: $FAEST_VERSION"
echo "- Updated on: $(date -u +%Y-%m-%d)"
echo ""

# Summary
echo "============================================================"
echo "✓ Release preparation complete!"
echo "============================================================"
echo ""
echo "Bundled libraries:"
ls -lh "$PYFAEST_DIR/lib/linux/x86_64/"*.so* 2>/dev/null || echo "  (none)"
echo ""
echo "Next steps:"
echo ""
echo "1. Update version in setup.py:"
echo "   version='1.0.1'  # or appropriate version"
echo ""
echo "2. Update CHANGELOG.md with release notes"
echo ""
echo "3. Test the build:"
echo "   python -m build"
echo "   pip install dist/pyfaest-*.tar.gz"
echo ""
echo "4. Test installation in clean environment:"
echo "   docker run -it python:3.11 bash"
echo "   pip install dist/pyfaest-*.whl"
echo ""
echo "5. Upload to TestPyPI:"
echo "   twine upload --repository testpypi dist/*"
echo ""
echo "6. Test from TestPyPI:"
echo "   pip install -i https://test.pypi.org/simple/ pyfaest"
echo ""
echo "7. Upload to PyPI:"
echo "   twine upload dist/*"
echo ""

# Note about multi-platform
echo "============================================================"
echo "MULTI-PLATFORM BUILDS"
echo "============================================================"
echo ""
echo "This script bundled the current platform only."
echo "For full PyPI release, you need to:"
echo ""
echo "1. Build on each platform (Linux, macOS, Windows)"
echo "2. Copy each platform's library to lib/<platform>/"
echo "3. Or use GitHub Actions with cibuildwheel"
echo ""
echo "See PUBLISHING_GUIDE.md for details"
echo ""
