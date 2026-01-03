"""
PyFAEST - Python wrapper for FAEST post-quantum signature scheme

This module provides a Pythonic interface to the FAEST C library.
Handles memory management, error handling, and type conversions.
"""

from typing import Tuple, Optional
import weakref

try:
    from _faest_cffi import ffi, lib
except ImportError:
    raise ImportError(
        "FAEST C library bindings not found. "
        "Please run 'python faest_build.py' to generate the bindings, "
        "or install the package with 'pip install .'"
    )


class FaestError(Exception):
    """Base exception for FAEST operations"""
    pass


class KeyGenerationError(FaestError):
    """Raised when key generation fails"""
    pass


class SignatureError(FaestError):
    """Raised when signature generation fails"""
    pass


class VerificationError(FaestError):
    """Raised when signature verification fails"""
    pass


class InvalidKeyPairError(FaestError):
    """Raised when keypair validation fails"""
    pass


# Parameter set configurations
PARAMETER_SETS = {
    '128f': {
        'pk_size': lib.FAEST_128F_PUBLIC_KEY_SIZE,
        'sk_size': lib.FAEST_128F_PRIVATE_KEY_SIZE,
        'sig_size': lib.FAEST_128F_SIGNATURE_SIZE,
        'keygen': lib.faest_128f_keygen,
        'sign': lib.faest_128f_sign,
        'verify': lib.faest_128f_verify,
        'validate': lib.faest_128f_validate_keypair,
        'clear': lib.faest_128f_clear_private_key,
    },
    '128s': {
        'pk_size': lib.FAEST_128S_PUBLIC_KEY_SIZE,
        'sk_size': lib.FAEST_128S_PRIVATE_KEY_SIZE,
        'sig_size': lib.FAEST_128S_SIGNATURE_SIZE,
        'keygen': lib.faest_128s_keygen,
        'sign': lib.faest_128s_sign,
        'verify': lib.faest_128s_verify,
        'validate': lib.faest_128s_validate_keypair,
        'clear': lib.faest_128s_clear_private_key,
    },
    '192f': {
        'pk_size': lib.FAEST_192F_PUBLIC_KEY_SIZE,
        'sk_size': lib.FAEST_192F_PRIVATE_KEY_SIZE,
        'sig_size': lib.FAEST_192F_SIGNATURE_SIZE,
        'keygen': lib.faest_192f_keygen,
        'sign': lib.faest_192f_sign,
        'verify': lib.faest_192f_verify,
        'validate': lib.faest_192f_validate_keypair,
        'clear': lib.faest_192f_clear_private_key,
    },
    '192s': {
        'pk_size': lib.FAEST_192S_PUBLIC_KEY_SIZE,
        'sk_size': lib.FAEST_192S_PRIVATE_KEY_SIZE,
        'sig_size': lib.FAEST_192S_SIGNATURE_SIZE,
        'keygen': lib.faest_192s_keygen,
        'sign': lib.faest_192s_sign,
        'verify': lib.faest_192s_verify,
        'validate': lib.faest_192s_validate_keypair,
        'clear': lib.faest_192s_clear_private_key,
    },
    '256f': {
        'pk_size': lib.FAEST_256F_PUBLIC_KEY_SIZE,
        'sk_size': lib.FAEST_256F_PRIVATE_KEY_SIZE,
        'sig_size': lib.FAEST_256F_SIGNATURE_SIZE,
        'keygen': lib.faest_256f_keygen,
        'sign': lib.faest_256f_sign,
        'verify': lib.faest_256f_verify,
        'validate': lib.faest_256f_validate_keypair,
        'clear': lib.faest_256f_clear_private_key,
    },
    '256s': {
        'pk_size': lib.FAEST_256S_PUBLIC_KEY_SIZE,
        'sk_size': lib.FAEST_256S_PRIVATE_KEY_SIZE,
        'sig_size': lib.FAEST_256S_SIGNATURE_SIZE,
        'keygen': lib.faest_256s_keygen,
        'sign': lib.faest_256s_sign,
        'verify': lib.faest_256s_verify,
        'validate': lib.faest_256s_validate_keypair,
        'clear': lib.faest_256s_clear_private_key,
    },
    'em_128f': {
        'pk_size': lib.FAEST_EM_128F_PUBLIC_KEY_SIZE,
        'sk_size': lib.FAEST_EM_128F_PRIVATE_KEY_SIZE,
        'sig_size': lib.FAEST_EM_128F_SIGNATURE_SIZE,
        'keygen': lib.faest_em_128f_keygen,
        'sign': lib.faest_em_128f_sign,
        'verify': lib.faest_em_128f_verify,
        'validate': lib.faest_em_128f_validate_keypair,
        'clear': lib.faest_em_128f_clear_private_key,
    },
    'em_128s': {
        'pk_size': lib.FAEST_EM_128S_PUBLIC_KEY_SIZE,
        'sk_size': lib.FAEST_EM_128S_PRIVATE_KEY_SIZE,
        'sig_size': lib.FAEST_EM_128S_SIGNATURE_SIZE,
        'keygen': lib.faest_em_128s_keygen,
        'sign': lib.faest_em_128s_sign,
        'verify': lib.faest_em_128s_verify,
        'validate': lib.faest_em_128s_validate_keypair,
        'clear': lib.faest_em_128s_clear_private_key,
    },
    'em_192f': {
        'pk_size': lib.FAEST_EM_192F_PUBLIC_KEY_SIZE,
        'sk_size': lib.FAEST_EM_192F_PRIVATE_KEY_SIZE,
        'sig_size': lib.FAEST_EM_192F_SIGNATURE_SIZE,
        'keygen': lib.faest_em_192f_keygen,
        'sign': lib.faest_em_192f_sign,
        'verify': lib.faest_em_192f_verify,
        'validate': lib.faest_em_192f_validate_keypair,
        'clear': lib.faest_em_192f_clear_private_key,
    },
    'em_192s': {
        'pk_size': lib.FAEST_EM_192S_PUBLIC_KEY_SIZE,
        'sk_size': lib.FAEST_EM_192S_PRIVATE_KEY_SIZE,
        'sig_size': lib.FAEST_EM_192S_SIGNATURE_SIZE,
        'keygen': lib.faest_em_192s_keygen,
        'sign': lib.faest_em_192s_sign,
        'verify': lib.faest_em_192s_verify,
        'validate': lib.faest_em_192s_validate_keypair,
        'clear': lib.faest_em_192s_clear_private_key,
    },
    'em_256f': {
        'pk_size': lib.FAEST_EM_256F_PUBLIC_KEY_SIZE,
        'sk_size': lib.FAEST_EM_256F_PRIVATE_KEY_SIZE,
        'sig_size': lib.FAEST_EM_256F_SIGNATURE_SIZE,
        'keygen': lib.faest_em_256f_keygen,
        'sign': lib.faest_em_256f_sign,
        'verify': lib.faest_em_256f_verify,
        'validate': lib.faest_em_256f_validate_keypair,
        'clear': lib.faest_em_256f_clear_private_key,
    },
    'em_256s': {
        'pk_size': lib.FAEST_EM_256S_PUBLIC_KEY_SIZE,
        'sk_size': lib.FAEST_EM_256S_PRIVATE_KEY_SIZE,
        'sig_size': lib.FAEST_EM_256S_SIGNATURE_SIZE,
        'keygen': lib.faest_em_256s_keygen,
        'sign': lib.faest_em_256s_sign,
        'verify': lib.faest_em_256s_verify,
        'validate': lib.faest_em_256s_validate_keypair,
        'clear': lib.faest_em_256s_clear_private_key,
    },
}


class PrivateKey:
    """
    Represents a FAEST private key with secure memory handling.
    
    The private key data is automatically cleared from memory when the object
    is garbage collected.
    """
    
    def __init__(self, key_bytes: bytes, param_set: str):
        """
        Initialize a private key.
        
        Args:
            key_bytes: The raw private key bytes
            param_set: The parameter set identifier (e.g., '128f', '256s')
        """
        if not isinstance(key_bytes, bytes):
            raise TypeError("Private key must be bytes")
        
        if param_set not in PARAMETER_SETS:
            raise ValueError(f"Invalid parameter set: {param_set}")
        
        self._params = PARAMETER_SETS[param_set]
        
        if len(key_bytes) != self._params['sk_size']:
            raise ValueError(
                f"Invalid private key size: expected {self._params['sk_size']}, "
                f"got {len(key_bytes)}"
            )
        
        self._param_set = param_set
        # Allocate C memory for the key
        self._sk_buf = ffi.new(f"uint8_t[{self._params['sk_size']}]")
        ffi.memmove(self._sk_buf, key_bytes, self._params['sk_size'])
        
        # Register cleanup to clear key on deletion
        self._finalizer = weakref.finalize(self, self._clear_key, 
                                          self._sk_buf, self._params['clear'])
    
    @staticmethod
    def _clear_key(sk_buf, clear_func):
        """Securely clear the private key from memory"""
        try:
            clear_func(sk_buf)
        except:
            pass  # Ignore errors during cleanup
    
    def to_bytes(self) -> bytes:
        """Export the private key as bytes (use with caution!)"""
        return bytes(ffi.buffer(self._sk_buf, self._params['sk_size']))
    
    @property
    def param_set(self) -> str:
        """Get the parameter set identifier"""
        return self._param_set
    
    def __del__(self):
        """Ensure cleanup happens"""
        if hasattr(self, '_finalizer'):
            self._finalizer()


class PublicKey:
    """Represents a FAEST public key"""
    
    def __init__(self, key_bytes: bytes, param_set: str):
        """
        Initialize a public key.
        
        Args:
            key_bytes: The raw public key bytes
            param_set: The parameter set identifier (e.g., '128f', '256s')
        """
        if not isinstance(key_bytes, bytes):
            raise TypeError("Public key must be bytes")
        
        if param_set not in PARAMETER_SETS:
            raise ValueError(f"Invalid parameter set: {param_set}")
        
        self._params = PARAMETER_SETS[param_set]
        
        if len(key_bytes) != self._params['pk_size']:
            raise ValueError(
                f"Invalid public key size: expected {self._params['pk_size']}, "
                f"got {len(key_bytes)}"
            )
        
        self._param_set = param_set
        self._pk_bytes = key_bytes
    
    def to_bytes(self) -> bytes:
        """Export the public key as bytes"""
        return self._pk_bytes
    
    @property
    def param_set(self) -> str:
        """Get the parameter set identifier"""
        return self._param_set
    
    def __bytes__(self) -> bytes:
        return self._pk_bytes
    
    def __repr__(self) -> str:
        return f"PublicKey(param_set='{self._param_set}', size={len(self._pk_bytes)})"


class Keypair:
    """
    Represents a FAEST keypair (public key + private key).
    
    Example:
        >>> keypair = Keypair.generate('128f')
        >>> pk_bytes = keypair.public_key.to_bytes()
        >>> sk_bytes = keypair.private_key.to_bytes()
    """
    
    def __init__(self, public_key: PublicKey, private_key: PrivateKey):
        """
        Initialize a keypair.
        
        Args:
            public_key: The public key
            private_key: The private key
        """
        if public_key.param_set != private_key.param_set:
            raise ValueError("Public and private keys must use the same parameter set")
        
        self.public_key = public_key
        self.private_key = private_key
    
    @classmethod
    def generate(cls, param_set: str = '128f') -> 'Keypair':
        """
        Generate a new keypair.
        
        Args:
            param_set: The parameter set to use (default: '128f')
                      Options: '128f', '128s', '192f', '192s', '256f', '256s',
                               'em_128f', 'em_128s', 'em_192f', 'em_192s', 
                               'em_256f', 'em_256s'
        
        Returns:
            A new Keypair instance
        
        Raises:
            KeyGenerationError: If key generation fails
        """
        if param_set not in PARAMETER_SETS:
            raise ValueError(
                f"Invalid parameter set: {param_set}. "
                f"Valid options: {', '.join(PARAMETER_SETS.keys())}"
            )
        
        params = PARAMETER_SETS[param_set]
        
        # Allocate buffers for the keys
        pk_buf = ffi.new(f"uint8_t[{params['pk_size']}]")
        sk_buf = ffi.new(f"uint8_t[{params['sk_size']}]")
        
        # Call C key generation function
        result = params['keygen'](pk_buf, sk_buf)
        
        if result != 0:
            raise KeyGenerationError(f"Key generation failed with error code {result}")
        
        # Convert C buffers to Python bytes
        pk_bytes = bytes(ffi.buffer(pk_buf, params['pk_size']))
        sk_bytes = bytes(ffi.buffer(sk_buf, params['sk_size']))
        
        # Create key objects
        public_key = PublicKey(pk_bytes, param_set)
        private_key = PrivateKey(sk_bytes, param_set)
        
        return cls(public_key, private_key)
    
    @classmethod
    def from_bytes(cls, public_key_bytes: bytes, private_key_bytes: bytes, 
                   param_set: str) -> 'Keypair':
        """
        Create a keypair from raw bytes.
        
        Args:
            public_key_bytes: The public key bytes
            private_key_bytes: The private key bytes
            param_set: The parameter set identifier
        
        Returns:
            A Keypair instance
        """
        public_key = PublicKey(public_key_bytes, param_set)
        private_key = PrivateKey(private_key_bytes, param_set)
        return cls(public_key, private_key)
    
    def validate(self) -> bool:
        """
        Validate that the keypair is correctly formed.
        
        Returns:
            True if the keypair is valid, False otherwise
        """
        params = PARAMETER_SETS[self.public_key.param_set]
        
        pk_buf = ffi.new(f"uint8_t[{params['pk_size']}]")
        ffi.memmove(pk_buf, self.public_key.to_bytes(), params['pk_size'])
        
        result = params['validate'](pk_buf, self.private_key._sk_buf)
        
        return result == 0
    
    @property
    def param_set(self) -> str:
        """Get the parameter set identifier"""
        return self.public_key.param_set


def sign(message: bytes, private_key: PrivateKey) -> bytes:
    """
    Sign a message with a private key.
    
    Args:
        message: The message to sign (as bytes)
        private_key: The private key to sign with
    
    Returns:
        The signature as bytes
    
    Raises:
        SignatureError: If signing fails
        TypeError: If inputs are not bytes
    """
    if not isinstance(message, bytes):
        raise TypeError("Message must be bytes")
    
    params = private_key._params
    
    # Allocate buffer for signature
    sig_buf = ffi.new(f"uint8_t[{params['sig_size']}]")
    sig_len = ffi.new("size_t*")
    sig_len[0] = params['sig_size']
    
    # Call C sign function
    result = params['sign'](
        private_key._sk_buf,
        message,
        len(message),
        sig_buf,
        sig_len
    )
    
    if result != 0:
        raise SignatureError(f"Signature generation failed with error code {result}")
    
    # Return only the actual signature bytes (not the full buffer)
    actual_sig_len = sig_len[0]
    return bytes(ffi.buffer(sig_buf, actual_sig_len))


def verify(message: bytes, signature: bytes, public_key: PublicKey) -> bool:
    """
    Verify a signature on a message.
    
    Args:
        message: The message that was signed
        signature: The signature to verify
        public_key: The public key to verify with
    
    Returns:
        True if the signature is valid, False otherwise
    
    Raises:
        TypeError: If inputs are not bytes
    """
    if not isinstance(message, bytes):
        raise TypeError("Message must be bytes")
    if not isinstance(signature, bytes):
        raise TypeError("Signature must be bytes")
    
    params = PARAMETER_SETS[public_key.param_set]
    
    # Prepare public key buffer
    pk_buf = ffi.new(f"uint8_t[{params['pk_size']}]")
    ffi.memmove(pk_buf, public_key.to_bytes(), params['pk_size'])
    
    # Call C verify function
    result = params['verify'](
        pk_buf,
        message,
        len(message),
        signature,
        len(signature)
    )
    
    # Return code 0 means valid signature
    return result == 0


__all__ = [
    'Keypair',
    'PublicKey',
    'PrivateKey',
    'sign',
    'verify',
    'FaestError',
    'KeyGenerationError',
    'SignatureError',
    'VerificationError',
    'InvalidKeyPairError',
    'PARAMETER_SETS',
]
