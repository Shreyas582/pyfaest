"""
Example demonstrating key serialization patterns

Shows various ways to save and load keys
"""

import json
import base64
from faest import Keypair, PublicKey, PrivateKey, sign, verify

def example_basic_serialization():
    """Basic key export/import"""
    print("\n" + "="*60)
    print("1. Basic Serialization (bytes)")
    print("="*60)
    
    # Generate keypair
    keypair = Keypair.generate('128f')
    
    # Export to bytes
    pk_bytes = keypair.public_key.to_bytes()
    sk_bytes = keypair.private_key.to_bytes()
    
    print(f"Public key:  {len(pk_bytes)} bytes")
    print(f"Private key: {len(sk_bytes)} bytes")
    
    # Reimport
    keypair_loaded = Keypair.from_bytes(pk_bytes, sk_bytes, '128f')
    
    # Verify it works
    message = b"Test message"
    signature = sign(message, keypair.private_key)
    is_valid = verify(message, signature, keypair_loaded.public_key)
    
    print(f"Verification after reload: {'✓ PASS' if is_valid else '✗ FAIL'}")

def example_hex_encoding():
    """Hex string encoding"""
    print("\n" + "="*60)
    print("2. Hex String Encoding")
    print("="*60)
    
    keypair = Keypair.generate('128s')
    
    # Convert to hex strings
    pk_hex = keypair.public_key.to_bytes().hex()
    sk_hex = keypair.private_key.to_bytes().hex()
    
    print(f"Public key (hex):  {pk_hex[:64]}...")
    print(f"Private key (hex): {sk_hex[:64]}...")
    
    # Convert back from hex
    pk_bytes = bytes.fromhex(pk_hex)
    sk_bytes = bytes.fromhex(sk_hex)
    
    keypair_loaded = Keypair.from_bytes(pk_bytes, sk_bytes, '128s')
    
    # Test
    message = b"Hex encoding test"
    signature = sign(message, keypair.private_key)
    is_valid = verify(message, signature, keypair_loaded.public_key)
    
    print(f"Verification after reload: {'✓ PASS' if is_valid else '✗ FAIL'}")

def example_base64_encoding():
    """Base64 encoding (for JSON, URLs, etc.)"""
    print("\n" + "="*60)
    print("3. Base64 Encoding (JSON-friendly)")
    print("="*60)
    
    keypair = Keypair.generate('192f')
    
    # Convert to base64
    pk_b64 = base64.b64encode(keypair.public_key.to_bytes()).decode('ascii')
    sk_b64 = base64.b64encode(keypair.private_key.to_bytes()).decode('ascii')
    
    print(f"Public key (base64):  {pk_b64[:60]}...")
    print(f"Private key (base64): {sk_b64[:60]}...")
    
    # Save to JSON
    key_data = {
        'param_set': '192f',
        'public_key': pk_b64,
        'private_key': sk_b64
    }
    
    json_str = json.dumps(key_data, indent=2)
    print(f"\nJSON representation:\n{json_str[:200]}...")
    
    # Load from JSON
    loaded_data = json.loads(json_str)
    pk_bytes = base64.b64decode(loaded_data['public_key'])
    sk_bytes = base64.b64decode(loaded_data['private_key'])
    
    keypair_loaded = Keypair.from_bytes(pk_bytes, sk_bytes, loaded_data['param_set'])
    
    # Test
    message = b"Base64 encoding test"
    signature = sign(message, keypair.private_key)
    is_valid = verify(message, signature, keypair_loaded.public_key)
    
    print(f"\nVerification after reload: {'✓ PASS' if is_valid else '✗ FAIL'}")

def example_file_storage():
    """Saving keys to files"""
    print("\n" + "="*60)
    print("4. File Storage")
    print("="*60)
    
    keypair = Keypair.generate('256s')
    
    # Save to files (binary format)
    with open('test_public.key', 'wb') as f:
        f.write(keypair.public_key.to_bytes())
    
    with open('test_private.key', 'wb') as f:
        f.write(keypair.private_key.to_bytes())
    
    print("✓ Keys saved to files:")
    print("  - test_public.key")
    print("  - test_private.key")
    
    # Load from files
    with open('test_public.key', 'rb') as f:
        pk_bytes = f.read()
    
    with open('test_private.key', 'rb') as f:
        sk_bytes = f.read()
    
    keypair_loaded = Keypair.from_bytes(pk_bytes, sk_bytes, '256s')
    
    # Test
    message = b"File storage test"
    signature = sign(message, keypair.private_key)
    is_valid = verify(message, signature, keypair_loaded.public_key)
    
    print(f"✓ Keys loaded from files")
    print(f"Verification after reload: {'✓ PASS' if is_valid else '✗ FAIL'}")
    
    # Cleanup
    import os
    os.remove('test_public.key')
    os.remove('test_private.key')
    print("✓ Test files cleaned up")

def example_public_key_only():
    """Working with public key only (for verification)"""
    print("\n" + "="*60)
    print("5. Public Key Only (Verification)")
    print("="*60)
    
    # Signer side: generate keypair and sign
    keypair = Keypair.generate('128f')
    message = b"Message to be verified remotely"
    signature = sign(message, keypair.private_key)
    
    # Export only public key (for distribution)
    pk_bytes = keypair.public_key.to_bytes()
    
    print(f"✓ Signature created: {len(signature)} bytes")
    print(f"✓ Public key exported: {len(pk_bytes)} bytes")
    
    # Verifier side: load public key only
    public_key = PublicKey(pk_bytes, '128f')
    
    # Verify without needing private key
    is_valid = verify(message, signature, public_key)
    
    print(f"✓ Verification (public key only): {'✓ PASS' if is_valid else '✗ FAIL'}")

def main():
    print("\n" + "="*70)
    print("PyFAEST - Key Serialization Examples")
    print("="*70)
    print("\nThis example demonstrates various ways to serialize/deserialize keys")
    
    try:
        example_basic_serialization()
        example_hex_encoding()
        example_base64_encoding()
        example_file_storage()
        example_public_key_only()
        
        print("\n" + "="*70)
        print("All serialization examples completed successfully!")
        print("="*70)
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
