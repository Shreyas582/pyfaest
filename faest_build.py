"""
CFFI Builder Script for PyFAEST
This script generates the Python bindings for the FAEST C library
Run this during the installation process
"""

from cffi import FFI
import os
import sys

ffibuilder = FFI()

# Read the API header and declare all functions to CFFI
# Note: We simplify the declarations for CFFI (no FAEST_EXPORT, FAEST_CALLING_CONVENTION)
ffibuilder.cdef("""
    /* FAEST-128F Parameter Set */
    #define FAEST_128F_PUBLIC_KEY_SIZE 32
    #define FAEST_128F_PRIVATE_KEY_SIZE 32
    #define FAEST_128F_SIGNATURE_SIZE 5924

    int faest_128f_keygen(uint8_t* pk, uint8_t* sk);
    int faest_128f_sign(const uint8_t* sk, const uint8_t* message, size_t message_len, 
                        uint8_t* signature, size_t* signature_len);
    int faest_128f_verify(const uint8_t* pk, const uint8_t* message, size_t message_len, 
                          const uint8_t* signature, size_t signature_len);
    int faest_128f_validate_keypair(const uint8_t* pk, const uint8_t* sk);
    void faest_128f_clear_private_key(uint8_t* key);

    /* FAEST-128S Parameter Set */
    #define FAEST_128S_PUBLIC_KEY_SIZE 32
    #define FAEST_128S_PRIVATE_KEY_SIZE 32
    #define FAEST_128S_SIGNATURE_SIZE 4506

    int faest_128s_keygen(uint8_t* pk, uint8_t* sk);
    int faest_128s_sign(const uint8_t* sk, const uint8_t* message, size_t message_len, 
                        uint8_t* signature, size_t* signature_len);
    int faest_128s_verify(const uint8_t* pk, const uint8_t* message, size_t message_len, 
                          const uint8_t* signature, size_t signature_len);
    int faest_128s_validate_keypair(const uint8_t* pk, const uint8_t* sk);
    void faest_128s_clear_private_key(uint8_t* key);

    /* FAEST-192F Parameter Set */
    #define FAEST_192F_PUBLIC_KEY_SIZE 48
    #define FAEST_192F_PRIVATE_KEY_SIZE 40
    #define FAEST_192F_SIGNATURE_SIZE 14948

    int faest_192f_keygen(uint8_t* pk, uint8_t* sk);
    int faest_192f_sign(const uint8_t* sk, const uint8_t* message, size_t message_len, 
                        uint8_t* signature, size_t* signature_len);
    int faest_192f_verify(const uint8_t* pk, const uint8_t* message, size_t message_len, 
                          const uint8_t* signature, size_t signature_len);
    int faest_192f_validate_keypair(const uint8_t* pk, const uint8_t* sk);
    void faest_192f_clear_private_key(uint8_t* key);

    /* FAEST-192S Parameter Set */
    #define FAEST_192S_PUBLIC_KEY_SIZE 48
    #define FAEST_192S_PRIVATE_KEY_SIZE 40
    #define FAEST_192S_SIGNATURE_SIZE 11260

    int faest_192s_keygen(uint8_t* pk, uint8_t* sk);
    int faest_192s_sign(const uint8_t* sk, const uint8_t* message, size_t message_len, 
                        uint8_t* signature, size_t* signature_len);
    int faest_192s_verify(const uint8_t* pk, const uint8_t* message, size_t message_len, 
                          const uint8_t* signature, size_t signature_len);
    int faest_192s_validate_keypair(const uint8_t* pk, const uint8_t* sk);
    void faest_192s_clear_private_key(uint8_t* key);

    /* FAEST-256F Parameter Set */
    #define FAEST_256F_PUBLIC_KEY_SIZE 48
    #define FAEST_256F_PRIVATE_KEY_SIZE 48
    #define FAEST_256F_SIGNATURE_SIZE 26548

    int faest_256f_keygen(uint8_t* pk, uint8_t* sk);
    int faest_256f_sign(const uint8_t* sk, const uint8_t* message, size_t message_len, 
                        uint8_t* signature, size_t* signature_len);
    int faest_256f_verify(const uint8_t* pk, const uint8_t* message, size_t message_len, 
                          const uint8_t* signature, size_t signature_len);
    int faest_256f_validate_keypair(const uint8_t* pk, const uint8_t* sk);
    void faest_256f_clear_private_key(uint8_t* key);

    /* FAEST-256S Parameter Set */
    #define FAEST_256S_PUBLIC_KEY_SIZE 48
    #define FAEST_256S_PRIVATE_KEY_SIZE 48
    #define FAEST_256S_SIGNATURE_SIZE 20696

    int faest_256s_keygen(uint8_t* pk, uint8_t* sk);
    int faest_256s_sign(const uint8_t* sk, const uint8_t* message, size_t message_len, 
                        uint8_t* signature, size_t* signature_len);
    int faest_256s_verify(const uint8_t* pk, const uint8_t* message, size_t message_len, 
                          const uint8_t* signature, size_t signature_len);
    int faest_256s_validate_keypair(const uint8_t* pk, const uint8_t* sk);
    void faest_256s_clear_private_key(uint8_t* key);

    /* EM (Extended Mode) Parameter Sets */

    /* FAEST-EM-128F */
    #define FAEST_EM_128F_PUBLIC_KEY_SIZE 32
    #define FAEST_EM_128F_PRIVATE_KEY_SIZE 32
    #define FAEST_EM_128F_SIGNATURE_SIZE 5060

    int faest_em_128f_keygen(uint8_t* pk, uint8_t* sk);
    int faest_em_128f_sign(const uint8_t* sk, const uint8_t* message, size_t message_len, 
                           uint8_t* signature, size_t* signature_len);
    int faest_em_128f_verify(const uint8_t* pk, const uint8_t* message, size_t message_len, 
                             const uint8_t* signature, size_t signature_len);
    int faest_em_128f_validate_keypair(const uint8_t* pk, const uint8_t* sk);
    void faest_em_128f_clear_private_key(uint8_t* key);

    /* FAEST-EM-128S */
    #define FAEST_EM_128S_PUBLIC_KEY_SIZE 32
    #define FAEST_EM_128S_PRIVATE_KEY_SIZE 32
    #define FAEST_EM_128S_SIGNATURE_SIZE 3906

    int faest_em_128s_keygen(uint8_t* pk, uint8_t* sk);
    int faest_em_128s_sign(const uint8_t* sk, const uint8_t* message, size_t message_len, 
                           uint8_t* signature, size_t* signature_len);
    int faest_em_128s_verify(const uint8_t* pk, const uint8_t* message, size_t message_len, 
                             const uint8_t* signature, size_t signature_len);
    int faest_em_128s_validate_keypair(const uint8_t* pk, const uint8_t* sk);
    void faest_em_128s_clear_private_key(uint8_t* key);

    /* FAEST-EM-192F */
    #define FAEST_EM_192F_PUBLIC_KEY_SIZE 48
    #define FAEST_EM_192F_PRIVATE_KEY_SIZE 48
    #define FAEST_EM_192F_SIGNATURE_SIZE 12380

    int faest_em_192f_keygen(uint8_t* pk, uint8_t* sk);
    int faest_em_192f_sign(const uint8_t* sk, const uint8_t* message, size_t message_len, 
                           uint8_t* signature, size_t* signature_len);
    int faest_em_192f_verify(const uint8_t* pk, const uint8_t* message, size_t message_len, 
                             const uint8_t* signature, size_t signature_len);
    int faest_em_192f_validate_keypair(const uint8_t* pk, const uint8_t* sk);
    void faest_em_192f_clear_private_key(uint8_t* key);

    /* FAEST-EM-192S */
    #define FAEST_EM_192S_PUBLIC_KEY_SIZE 48
    #define FAEST_EM_192S_PRIVATE_KEY_SIZE 48
    #define FAEST_EM_192S_SIGNATURE_SIZE 9340

    int faest_em_192s_keygen(uint8_t* pk, uint8_t* sk);
    int faest_em_192s_sign(const uint8_t* sk, const uint8_t* message, size_t message_len, 
                           uint8_t* signature, size_t* signature_len);
    int faest_em_192s_verify(const uint8_t* pk, const uint8_t* message, size_t message_len, 
                             const uint8_t* signature, size_t signature_len);
    int faest_em_192s_validate_keypair(const uint8_t* pk, const uint8_t* sk);
    void faest_em_192s_clear_private_key(uint8_t* key);

    /* FAEST-EM-256F */
    #define FAEST_EM_256F_PUBLIC_KEY_SIZE 64
    #define FAEST_EM_256F_PRIVATE_KEY_SIZE 64
    #define FAEST_EM_256F_SIGNATURE_SIZE 23476

    int faest_em_256f_keygen(uint8_t* pk, uint8_t* sk);
    int faest_em_256f_sign(const uint8_t* sk, const uint8_t* message, size_t message_len, 
                           uint8_t* signature, size_t* signature_len);
    int faest_em_256f_verify(const uint8_t* pk, const uint8_t* message, size_t message_len, 
                             const uint8_t* signature, size_t signature_len);
    int faest_em_256f_validate_keypair(const uint8_t* pk, const uint8_t* sk);
    void faest_em_256f_clear_private_key(uint8_t* key);

    /* FAEST-EM-256S */
    #define FAEST_EM_256S_PUBLIC_KEY_SIZE 64
    #define FAEST_EM_256S_PRIVATE_KEY_SIZE 64
    #define FAEST_EM_256S_SIGNATURE_SIZE 17984

    int faest_em_256s_keygen(uint8_t* pk, uint8_t* sk);
    int faest_em_256s_sign(const uint8_t* sk, const uint8_t* message, size_t message_len, 
                           uint8_t* signature, size_t* signature_len);
    int faest_em_256s_verify(const uint8_t* pk, const uint8_t* message, size_t message_len, 
                             const uint8_t* signature, size_t signature_len);
    int faest_em_256s_validate_keypair(const uint8_t* pk, const uint8_t* sk);
    void faest_em_256s_clear_private_key(uint8_t* key);
""")

# Determine paths with priority:
# 1. Bundled libraries (for PyPI distribution)
# 2. Environment variables (for development with external faest-ref)
# 3. Relative paths (for development as subdirectory of faest-ref)

script_dir = os.path.dirname(os.path.abspath(__file__))

# Detect platform for bundled libraries
import platform
system = platform.system().lower()
machine = platform.machine().lower()

if system == 'linux':
    platform_dir = f'linux/{machine}' if machine in ['x86_64', 'aarch64'] else 'linux/x86_64'
elif system == 'darwin':
    platform_dir = f'macos/{machine}' if machine == 'arm64' else 'macos/x86_64'
elif system == 'windows':
    platform_dir = 'windows/x64'
else:
    platform_dir = None

# Check for bundled libraries first (PyPI install)
bundled_lib_dir = os.path.join(script_dir, 'lib', platform_dir) if platform_dir else None
bundled_include_dir = os.path.join(script_dir, 'include')

# Check if bundled libraries exist and have actual library files
has_bundled_libs = False
if bundled_lib_dir and os.path.exists(bundled_lib_dir) and os.path.exists(bundled_include_dir):
    # Verify at least one library file exists
    lib_files = []
    if os.path.exists(bundled_lib_dir):
        lib_files = [f for f in os.listdir(bundled_lib_dir) if f.startswith('libfaest')]
    
    if lib_files:
        has_bundled_libs = True

if has_bundled_libs:
    # Use bundled libraries (installed from PyPI or after running prepare_release.sh)
    build_dir = bundled_lib_dir
    src_dir = bundled_include_dir
    print(f"Using bundled FAEST library (PyPI distribution)")
    print(f"  Library directory: {build_dir}")
    print(f"  Headers directory: {src_dir}")
else:
    # Development mode: check environment variables or relative paths
    build_dir = os.environ.get('FAEST_BUILD_DIR', os.path.join(script_dir, '..', 'build'))
    src_dir = os.environ.get('FAEST_SRC_DIR', os.path.join(script_dir, '..'))
    
    # Validate paths
    if not os.path.exists(build_dir):
        print(f"ERROR: FAEST build directory not found: {build_dir}", file=sys.stderr)
        print("", file=sys.stderr)
        print("For development, either:", file=sys.stderr)
        print("  1. Set environment variables:", file=sys.stderr)
        print("     export FAEST_BUILD_DIR=/path/to/faest-ref/build", file=sys.stderr)
        print("     export FAEST_SRC_DIR=/path/to/faest-ref", file=sys.stderr)
        print("  2. Or run: ./scripts/prepare_release.sh to bundle libraries", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(src_dir):
        print(f"ERROR: FAEST source directory not found: {src_dir}", file=sys.stderr)
        print("Please set FAEST_SRC_DIR environment variable to the path containing FAEST headers", file=sys.stderr)
        print("Example: export FAEST_SRC_DIR=/path/to/faest-ref", file=sys.stderr)
        sys.exit(1)
    
    print(f"Using external FAEST library (development mode)")
    print(f"  Build directory: {build_dir}")
    print(f"  Source directory: {src_dir}")

# Configure the source module
ffibuilder.set_source(
    "_faest_cffi",  # Name of the generated Python module
    """
        #include "faest_128f.h"
        #include "faest_128s.h"
        #include "faest_192f.h"
        #include "faest_192s.h"
        #include "faest_256f.h"
        #include "faest_256s.h"
        #include "faest_em_128f.h"
        #include "faest_em_128s.h"
        #include "faest_em_192f.h"
        #include "faest_em_192s.h"
        #include "faest_em_256f.h"
        #include "faest_em_256s.h"
    """,
    libraries=['faest'],  # Link to libfaest.so / libfaest.dll / libfaest.a
    library_dirs=[build_dir],  # Where to find the library
    include_dirs=[build_dir, src_dir],  # Where to find the headers (both build and source)
    runtime_library_dirs=[build_dir] if system in ['linux', 'darwin'] else None,  # Set rpath for runtime library search
)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
