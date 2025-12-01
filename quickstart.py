#!/usr/bin/env python3
"""
Quick start script for PyFAEST
Demonstrates the most common use case in a single file
"""

from faest import Keypair, sign, verify

def main():
    # Choose a parameter set
    # Options: '128f', '128s', '192f', '192s', '256f', '256s'
    # 'f' = fast, 's' = small signatures
    PARAM_SET = '128f'
    
    print("PyFAEST Quick Start")
    print("=" * 50)
    
    # 1. Generate a keypair
    print("\n1. Generating keypair...")
    keypair = Keypair.generate(PARAM_SET)
    print(f"   Public key:  {len(keypair.public_key.to_bytes())} bytes")
    print(f"   Private key: {len(keypair.private_key.to_bytes())} bytes")
    
    # 2. Sign a message
    print("\n2. Signing a message...")
    message = b"Hello from PyFAEST!"
    signature = sign(message, keypair.private_key)
    print(f"   Message: {message.decode()}")
    print(f"   Signature: {len(signature)} bytes")
    
    # 3. Verify the signature
    print("\n3. Verifying signature...")
    is_valid = verify(message, signature, keypair.public_key)
    print(f"   Result: {'✓ VALID' if is_valid else '✗ INVALID'}")
    
    # 4. Test with wrong message (should fail)
    print("\n4. Testing with wrong message...")
    wrong_message = b"This is not the original message"
    is_valid = verify(wrong_message, signature, keypair.public_key)
    print(f"   Result: {'✓ VALID' if is_valid else '✗ INVALID (expected)'}")
    
    # 5. Export keys (for storage/transmission)
    print("\n5. Exporting keys...")
    pk_hex = keypair.public_key.to_bytes().hex()
    sk_hex = keypair.private_key.to_bytes().hex()
    print(f"   Public key (hex):  {pk_hex[:32]}...")
    print(f"   Private key (hex): {sk_hex[:32]}...")
    
    # 6. Import keys back
    print("\n6. Importing keys...")
    from faest import PublicKey, PrivateKey
    
    pk_imported = PublicKey(bytes.fromhex(pk_hex), PARAM_SET)
    sk_imported = PrivateKey(bytes.fromhex(sk_hex), PARAM_SET)
    
    # Verify with imported key
    is_valid = verify(message, signature, pk_imported)
    print(f"   Verification with imported key: {'✓ VALID' if is_valid else '✗ INVALID'}")
    
    print("\n" + "=" * 50)
    print("All operations completed successfully!")
    print("\nNext steps:")
    print("  - Check out examples/ directory for more examples")
    print("  - Read README.md for API documentation")
    print("  - Try other parameter sets: '128s', '192f', '256f', etc.")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nIf you see an ImportError, try:")
        print("  1. pip install -e .")
        print("  2. python faest_build.py")
        import traceback
        traceback.print_exc()
