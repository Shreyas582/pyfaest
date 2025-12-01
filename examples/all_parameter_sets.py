"""
Example demonstrating all FAEST parameter sets

Tests each parameter set to ensure compatibility and show size differences
"""

from faest import Keypair, sign, verify, PARAMETER_SETS

def test_parameter_set(param_set_name):
    """Test a specific parameter set"""
    print(f"\n{'='*70}")
    print(f"Testing FAEST-{param_set_name.upper()}")
    print('='*70)
    
    # Generate keypair
    keypair = Keypair.generate(param_set_name)
    
    # Get sizes
    pk_size = len(keypair.public_key.to_bytes())
    sk_size = len(keypair.private_key.to_bytes())
    
    print(f"  Public key:  {pk_size:5d} bytes")
    print(f"  Private key: {sk_size:5d} bytes")
    
    # Sign a test message
    message = b"Test message for FAEST signature scheme"
    signature = sign(message, keypair.private_key)
    
    print(f"  Signature:   {len(signature):5d} bytes")
    
    # Verify
    is_valid = verify(message, signature, keypair.public_key)
    print(f"  Verification: {'✓ PASS' if is_valid else '✗ FAIL'}")
    
    # Test with wrong message
    wrong_message = b"Different message"
    is_invalid = not verify(wrong_message, signature, keypair.public_key)
    print(f"  Invalid test: {'✓ PASS' if is_invalid else '✗ FAIL'}")
    
    return {
        'param_set': param_set_name,
        'pk_size': pk_size,
        'sk_size': sk_size,
        'sig_size': len(signature),
        'success': is_valid and is_invalid
    }

def main():
    print("\n" + "="*70)
    print("PyFAEST - All Parameter Sets Demonstration")
    print("="*70)
    
    results = []
    
    # Test standard parameter sets
    standard_sets = ['128f', '128s', '192f', '192s', '256f', '256s']
    
    print("\n🔷 STANDARD PARAMETER SETS")
    for param_set in standard_sets:
        try:
            result = test_parameter_set(param_set)
            results.append(result)
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
    
    # Test extended mode parameter sets
    em_sets = ['em_128f', 'em_128s', 'em_192f', 'em_192s', 'em_256f', 'em_256s']
    
    print("\n🔷 EXTENDED MODE (EM) PARAMETER SETS")
    for param_set in em_sets:
        try:
            result = test_parameter_set(param_set)
            results.append(result)
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
    
    # Summary table
    print("\n" + "="*70)
    print("SUMMARY TABLE")
    print("="*70)
    print(f"{'Parameter Set':<15} {'PK (bytes)':<12} {'SK (bytes)':<12} {'Sig (bytes)':<12} {'Status'}")
    print("-"*70)
    
    for result in results:
        status = '✓ PASS' if result['success'] else '✗ FAIL'
        print(f"{result['param_set']:<15} {result['pk_size']:<12} {result['sk_size']:<12} "
              f"{result['sig_size']:<12} {status}")
    
    print("="*70)
    
    # Success summary
    total = len(results)
    passed = sum(1 for r in results if r['success'])
    
    print(f"\nResults: {passed}/{total} parameter sets passed all tests")
    
    if passed == total:
        print("✓ All parameter sets working correctly!")
    else:
        print("✗ Some parameter sets failed")

if __name__ == '__main__':
    main()
