#!/bin/bash
# Update bundled FAEST libraries when faest-ref is updated
# Run this when you want to sync with a newer FAEST version

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYFAEST_DIR="$(dirname "$SCRIPT_DIR")"
FAEST_REF="${FAEST_REF:-$(dirname "$PYFAEST_DIR")}"

echo "============================================================"
echo "Updating FAEST Libraries"
echo "============================================================"
echo ""
echo "FAEST-ref: $FAEST_REF"
echo "PyFAEST:   $PYFAEST_DIR"
echo ""

# Check if FAEST build exists
if [ ! -d "$FAEST_REF/build" ]; then
    echo "ERROR: FAEST build directory not found"
    echo "Please build FAEST first or set FAEST_REF environment variable"
    exit 1
fi

# Update libraries
echo "Copying libraries..."
cp "$FAEST_REF/build/libfaest.so.1.0.0" "$PYFAEST_DIR/lib/linux/x86_64/" || \
    { echo "ERROR: Failed to copy library"; exit 1; }

cd "$PYFAEST_DIR/lib/linux/x86_64"
ln -sf libfaest.so.1.0.0 libfaest.so.1
ln -sf libfaest.so.1 libfaest.so
cd - > /dev/null
echo "  ✓ Library updated"

# Update headers
echo ""
echo "Copying headers..."
cp "$FAEST_REF/build"/*.h "$PYFAEST_DIR/include/" 2>/dev/null || true
cp "$FAEST_REF"/*.h "$PYFAEST_DIR/include/" 2>/dev/null || true
echo "  ✓ Headers updated"

# Record version
cd "$FAEST_REF"
if git rev-parse --git-dir > /dev/null 2>&1; then
    FAEST_VERSION=$(git describe --tags 2>/dev/null || git rev-parse --short HEAD)
    echo ""
    echo "FAEST version: $FAEST_VERSION"
    echo "FAEST_VERSION=$FAEST_VERSION" > "$PYFAEST_DIR/FAEST_VERSION.txt"
    echo "FAEST_COMMIT=$(git rev-parse HEAD)" >> "$PYFAEST_DIR/FAEST_VERSION.txt"
    echo "UPDATED_DATE=$(date -u +%Y-%m-%d)" >> "$PYFAEST_DIR/FAEST_VERSION.txt"
fi

cd "$PYFAEST_DIR"

echo ""
echo "============================================================"
echo "✓ Libraries updated successfully"
echo "============================================================"
echo ""
echo "Next steps:"
echo "1. Test the updated library:"
echo "   pip install --force-reinstall -e ."
echo "   python verify_install.py"
echo ""
echo "2. If tests pass, increment version in setup.py"
echo "3. Update CHANGELOG.md with FAEST version"
echo "4. Commit and create release"
echo ""
