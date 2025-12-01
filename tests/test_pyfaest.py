"""
Test suite for PyFAEST

Run with: pytest tests/
"""

import pytest
from faest import (
    Keypair, PublicKey, PrivateKey, sign, verify,
    KeyGenerationError, SignatureError, FaestError,
    PARAMETER_SETS
)


class TestKeyGeneration:
    """Test key generation functionality"""
    
    def test_generate_128f(self):
        """Test generating FAEST-128f keypair"""
        keypair = Keypair.generate('128f')
        assert keypair is not None
        assert keypair.public_key is not None
        assert keypair.private_key is not None
        assert keypair.param_set == '128f'
    
    def test_generate_all_parameter_sets(self):
        """Test generating keys for all parameter sets"""
        for param_set in PARAMETER_SETS.keys():
            keypair = Keypair.generate(param_set)
            assert keypair.param_set == param_set
    
    def test_invalid_parameter_set(self):
        """Test that invalid parameter set raises error"""
        with pytest.raises(ValueError):
            Keypair.generate('invalid_param')
    
    def test_key_sizes(self):
        """Test that generated keys have correct sizes"""
        keypair = Keypair.generate('128f')
        assert len(keypair.public_key.to_bytes()) == 32
        assert len(keypair.private_key.to_bytes()) == 32
    
    def test_keypair_validation(self):
        """Test keypair validation"""
        keypair = Keypair.generate('128f')
        assert keypair.validate() == True


class TestSigning:
    """Test signature generation"""
    
    def test_basic_signing(self):
        """Test basic message signing"""
        keypair = Keypair.generate('128f')
        message = b"Test message"
        signature = sign(message, keypair.private_key)
        assert signature is not None
        assert len(signature) > 0
        assert isinstance(signature, bytes)
    
    def test_empty_message(self):
        """Test signing empty message"""
        keypair = Keypair.generate('128f')
        message = b""
        signature = sign(message, keypair.private_key)
        assert signature is not None
    
    def test_long_message(self):
        """Test signing a long message"""
        keypair = Keypair.generate('128f')
        message = b"A" * 10000
        signature = sign(message, keypair.private_key)
        assert signature is not None
    
    def test_signature_sizes(self):
        """Test that signatures have expected sizes"""
        test_cases = [
            ('128f', 5924),
            ('128s', 4506),
            ('192f', 14948),
        ]
        
        for param_set, expected_size in test_cases:
            keypair = Keypair.generate(param_set)
            signature = sign(b"test", keypair.private_key)
            assert len(signature) == expected_size
    
    def test_type_checking(self):
        """Test that non-bytes input raises TypeError"""
        keypair = Keypair.generate('128f')
        with pytest.raises(TypeError):
            sign("string instead of bytes", keypair.private_key)


class TestVerification:
    """Test signature verification"""
    
    def test_valid_signature(self):
        """Test verifying a valid signature"""
        keypair = Keypair.generate('128f')
        message = b"Test message"
        signature = sign(message, keypair.private_key)
        assert verify(message, signature, keypair.public_key) == True
    
    def test_invalid_signature_wrong_message(self):
        """Test that wrong message fails verification"""
        keypair = Keypair.generate('128f')
        message = b"Original message"
        signature = sign(message, keypair.private_key)
        
        wrong_message = b"Different message"
        assert verify(wrong_message, signature, keypair.public_key) == False
    
    def test_invalid_signature_corrupted(self):
        """Test that corrupted signature fails verification"""
        keypair = Keypair.generate('128f')
        message = b"Test message"
        signature = sign(message, keypair.private_key)
        
        # Corrupt the signature
        corrupted_sig = bytearray(signature)
        corrupted_sig[0] ^= 0xFF
        corrupted_sig = bytes(corrupted_sig)
        
        assert verify(message, corrupted_sig, keypair.public_key) == False
    
    def test_invalid_signature_wrong_key(self):
        """Test that wrong public key fails verification"""
        keypair1 = Keypair.generate('128f')
        keypair2 = Keypair.generate('128f')
        
        message = b"Test message"
        signature = sign(message, keypair1.private_key)
        
        assert verify(message, signature, keypair2.public_key) == False
    
    def test_verify_type_checking(self):
        """Test type checking in verify function"""
        keypair = Keypair.generate('128f')
        message = b"test"
        signature = sign(message, keypair.private_key)
        
        with pytest.raises(TypeError):
            verify("not bytes", signature, keypair.public_key)
        
        with pytest.raises(TypeError):
            verify(message, "not bytes", keypair.public_key)


class TestSerialization:
    """Test key serialization and deserialization"""
    
    def test_public_key_serialization(self):
        """Test public key export and import"""
        keypair = Keypair.generate('128f')
        pk_bytes = keypair.public_key.to_bytes()
        
        assert isinstance(pk_bytes, bytes)
        assert len(pk_bytes) == 32
        
        # Create new public key from bytes
        pk2 = PublicKey(pk_bytes, '128f')
        assert pk2.to_bytes() == pk_bytes
    
    def test_private_key_serialization(self):
        """Test private key export and import"""
        keypair = Keypair.generate('128f')
        sk_bytes = keypair.private_key.to_bytes()
        
        assert isinstance(sk_bytes, bytes)
        assert len(sk_bytes) == 32
        
        # Create new private key from bytes
        sk2 = PrivateKey(sk_bytes, '128f')
        assert sk2.to_bytes() == sk_bytes
    
    def test_keypair_serialization(self):
        """Test complete keypair serialization"""
        keypair = Keypair.generate('128f')
        
        pk_bytes = keypair.public_key.to_bytes()
        sk_bytes = keypair.private_key.to_bytes()
        
        # Recreate keypair
        keypair2 = Keypair.from_bytes(pk_bytes, sk_bytes, '128f')
        
        # Test that it works
        message = b"Test after serialization"
        signature = sign(message, keypair.private_key)
        assert verify(message, signature, keypair2.public_key) == True
    
    def test_serialization_preserves_functionality(self):
        """Test that serialized keys still work correctly"""
        keypair = Keypair.generate('192f')
        message = b"Test message"
        
        # Sign with original key
        signature = sign(message, keypair.private_key)
        
        # Serialize and deserialize
        pk_bytes = keypair.public_key.to_bytes()
        sk_bytes = keypair.private_key.to_bytes()
        keypair2 = Keypair.from_bytes(pk_bytes, sk_bytes, '192f')
        
        # Verify with deserialized key
        assert verify(message, signature, keypair2.public_key) == True
        
        # Sign with deserialized key
        signature2 = sign(message, keypair2.private_key)
        assert verify(message, signature2, keypair.public_key) == True


class TestParameterSets:
    """Test all parameter sets"""
    
    @pytest.mark.parametrize("param_set", list(PARAMETER_SETS.keys()))
    def test_parameter_set_basic_operations(self, param_set):
        """Test basic operations for each parameter set"""
        # Generate keypair
        keypair = Keypair.generate(param_set)
        
        # Sign message
        message = b"Test message for " + param_set.encode()
        signature = sign(message, keypair.private_key)
        
        # Verify signature
        assert verify(message, signature, keypair.public_key) == True
        
        # Verify rejection of wrong message
        wrong_message = b"Wrong message"
        assert verify(wrong_message, signature, keypair.public_key) == False


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_mismatched_parameter_sets(self):
        """Test that mismatched parameter sets are handled"""
        keypair_128f = Keypair.generate('128f')
        
        # Can't create PublicKey with wrong param set
        with pytest.raises(ValueError):
            PublicKey(keypair_128f.public_key.to_bytes(), '256f')
    
    def test_invalid_key_size(self):
        """Test that invalid key sizes raise errors"""
        with pytest.raises(ValueError):
            PublicKey(b"too short", '128f')
        
        with pytest.raises(ValueError):
            PrivateKey(b"also too short", '128f')
    
    def test_key_type_checking(self):
        """Test type checking for keys"""
        with pytest.raises(TypeError):
            PublicKey("not bytes", '128f')
        
        with pytest.raises(TypeError):
            PrivateKey(12345, '128f')


class TestMemorySafety:
    """Test memory safety features"""
    
    def test_private_key_clearing(self):
        """Test that private keys are cleared on deletion"""
        keypair = Keypair.generate('128f')
        sk = keypair.private_key
        
        # Get a reference to the internal buffer
        sk_buf = sk._sk_buf
        
        # Delete the key
        del sk
        
        # The finalizer should have been called
        # (We can't easily verify the memory was zeroed, but we test it doesn't crash)
    
    def test_multiple_keypairs(self):
        """Test creating and destroying multiple keypairs"""
        keypairs = []
        for i in range(10):
            keypair = Keypair.generate('128f')
            keypairs.append(keypair)
        
        # Delete all at once
        keypairs.clear()
        
        # Should not cause any issues


class TestCrossParameterSet:
    """Test interactions between parameter sets"""
    
    def test_same_message_different_param_sets(self):
        """Test signing the same message with different parameter sets"""
        message = b"Same message for all"
        
        keypair_128f = Keypair.generate('128f')
        keypair_256s = Keypair.generate('256s')
        
        sig_128f = sign(message, keypair_128f.private_key)
        sig_256s = sign(message, keypair_256s.private_key)
        
        # Signatures should be different
        assert sig_128f != sig_256s
        
        # Each should verify with correct key
        assert verify(message, sig_128f, keypair_128f.public_key) == True
        assert verify(message, sig_256s, keypair_256s.public_key) == True
        
        # Should not cross-verify
        assert verify(message, sig_128f, keypair_256s.public_key) == False
        assert verify(message, sig_256s, keypair_128f.public_key) == False


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
