"""
Quick verification script to test if PyFAEST is working correctly
Run this after installation to verify everything is set up properly
"""

def test_import():
    """Test that the module can be imported"""
    print("1. Testing import...", end=" ")
    try:
        from faest import Keypair, sign, verify
        print("✓ PASS")
        return True
    except ImportError as e:
        print(f"✗ FAIL: {e}")
        return False

def test_key_generation():
    """Test key generation"""
    print("2. Testing key generation...", end=" ")
    try:
        from faest import Keypair
        keypair = Keypair.generate('128f')
        print("✓ PASS")
        return True
    except Exception as e:
        print(f"✗ FAIL: {e}")
        return False

def test_signing():
    """Test signing"""
    print("3. Testing signing...", end=" ")
    try:
        from faest import Keypair, sign
        keypair = Keypair.generate('128f')
        message = b"Test message"
        signature = sign(message, keypair.private_key)
        print("✓ PASS")
        return True
    except Exception as e:
        print(f"✗ FAIL: {e}")
        return False

def test_verification():
    """Test verification"""
    print("4. Testing verification...", end=" ")
    try:
        from faest import Keypair, sign, verify
        keypair = Keypair.generate('128f')
        message = b"Test message"
        signature = sign(message, keypair.private_key)
        is_valid = verify(message, signature, keypair.public_key)
        
        if is_valid:
            print("✓ PASS")
            return True
        else:
            print("✗ FAIL: Signature verification returned False")
            return False
    except Exception as e:
        print(f"✗ FAIL: {e}")
        return False

def test_serialization():
    """Test key serialization"""
    print("5. Testing serialization...", end=" ")
    try:
        from faest import Keypair
        keypair = Keypair.generate('128f')
        
        pk_bytes = keypair.public_key.to_bytes()
        sk_bytes = keypair.private_key.to_bytes()
        
        keypair2 = Keypair.from_bytes(pk_bytes, sk_bytes, '128f')
        
        print("✓ PASS")
        return True
    except Exception as e:
        print(f"✗ FAIL: {e}")
        return False

def main():
    print("="*60)
    print("PyFAEST Verification Script")
    print("="*60)
    print()
    
    tests = [
        test_import,
        test_key_generation,
        test_signing,
        test_verification,
        test_serialization,
    ]
    
    results = [test() for test in tests]
    
    print()
    print("="*60)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✓ All tests passed ({passed}/{total})")
        print("PyFAEST is working correctly!")
        print()
        print("Next steps:")
        print("  - Try: python examples/basic_usage.py")
        print("  - Try: python examples/all_parameter_sets.py")
        print("  - Try: pytest tests/ -v")
    else:
        print(f"✗ Some tests failed ({passed}/{total} passed)")
        print()
        print("Troubleshooting:")
        print("  1. Make sure CFFI is installed: pip install cffi")
        print("  2. Try rebuilding: python faest_build.py")
        print("  3. Check library path in faest_build.py")
        print("  4. See INSTALLATION.md for detailed help")
    
    print("="*60)
    
    return passed == total

if __name__ == '__main__':
    import sys
    success = main()
    sys.exit(0 if success else 1)
