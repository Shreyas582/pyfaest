"""
PyFAEST - Python bindings for FAEST post-quantum signature scheme

FAEST (Fast AES-based Signature with Tight security) is a post-quantum
digital signature scheme based on symmetric cryptography.

Example usage:
    >>> from faest import Keypair, sign, verify
    >>> 
    >>> # Generate a keypair
    >>> keypair = Keypair.generate('128f')
    >>> 
    >>> # Sign a message
    >>> message = b"Hello, quantum-resistant world!"
    >>> signature = sign(message, keypair.private_key)
    >>> 
    >>> # Verify the signature
    >>> is_valid = verify(message, signature, keypair.public_key)
    >>> print(f"Signature valid: {is_valid}")

Available parameter sets:
    - '128f': FAEST-128f (fast, ~128-bit security)
    - '128s': FAEST-128s (small, ~128-bit security)
    - '192f': FAEST-192f (fast, ~192-bit security)
    - '192s': FAEST-192s (small, ~192-bit security)
    - '256f': FAEST-256f (fast, ~256-bit security)
    - '256s': FAEST-256s (small, ~256-bit security)
    - 'em_128f', 'em_128s', 'em_192f', 'em_192s', 'em_256f', 'em_256s': Extended mode variants
"""

__version__ = '1.0.1'
__author__ = 'PyFAEST Contributors'

from .core import (
    Keypair,
    PublicKey,
    PrivateKey,
    sign,
    verify,
    FaestError,
    KeyGenerationError,
    SignatureError,
    VerificationError,
    InvalidKeyPairError,
    PARAMETER_SETS,
)

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
