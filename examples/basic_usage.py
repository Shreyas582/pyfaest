"""
Basic usage example for PyFAEST

This example demonstrates the fundamental operations:
- Key generation
- Message signing
- Signature verification
"""

from faest import Keypair, sign, verify

def main():
    print("=" * 60)
    print("PyFAEST Basic Usage Example")
    print("=" * 60)
    
    # Choose a parameter set
    param_set = '128f'  # Fast variant with ~128-bit security
    print(f"\nUsing parameter set: FAEST-{param_set.upper()}")
    
    # Generate a keypair
    print("\n1. Generating keypair...")
    keypair = Keypair.generate(param_set)
    print(f"   ✓ Public key size: {len(keypair.public_key.to_bytes())} bytes")
    print(f"   ✓ Private key size: {len(keypair.private_key.to_bytes())} bytes")
    
    # Validate the keypair
    print("\n2. Validating keypair...")
    is_valid = keypair.validate()
    print(f"   ✓ Keypair is {'valid' if is_valid else 'INVALID'}")
    
    # Sign a message
    message = b"Hello, quantum-resistant world!"
    print(f"\n3. Signing message: {message.decode()}")
    signature = sign(message, keypair.private_key)
    print(f"   ✓ Signature size: {len(signature)} bytes")
    
    # Verify the signature
    print("\n4. Verifying signature...")
    is_valid = verify(message, signature, keypair.public_key)
    print(f"   ✓ Signature is {'VALID' if is_valid else 'invalid'}")
    
    # Try to verify with a tampered message
    print("\n5. Testing with tampered message...")
    tampered_message = b"Goodbye, quantum-resistant world!"
    is_valid = verify(tampered_message, signature, keypair.public_key)
    print(f"   ✓ Signature is {'valid' if is_valid else 'INVALID (as expected)'}")
    
    # Export and reimport keys
    print("\n6. Testing key serialization...")
    pk_bytes = keypair.public_key.to_bytes()
    sk_bytes = keypair.private_key.to_bytes()
    
    keypair2 = Keypair.from_bytes(pk_bytes, sk_bytes, param_set)
    print("   ✓ Keys exported and reimported")
    
    # Verify with reimported keys
    is_valid = verify(message, signature, keypair2.public_key)
    print(f"   ✓ Verification with reimported key: {'VALID' if is_valid else 'invalid'}")
    
    print("\n" + "=" * 60)
    print("All operations completed successfully!")
    print("=" * 60)

if __name__ == '__main__':
    main()
