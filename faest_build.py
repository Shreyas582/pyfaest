"""
CFFI Builder Script for PyFAEST
This script generates the Python bindings for the FAEST C library
Run this during the installation process
"""

from cffi import FFI
import os
import sys
import subprocess
import urllib.request
import tarfile
import zipfile

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

# Note: When running sdist, cffi_modules is empty so this script won't be executed

# Determine paths with priority:
# 1. Bundled libraries (for PyPI distribution)
# 2. Environment variables (for development with external faest-ref)
# 3. Relative paths (for development as subdirectory of faest-ref)

script_dir = os.path.dirname(os.path.abspath(__file__))

# Detect platform for bundled libraries
import platform
system = platform.system().lower()
machine = platform.machine().lower()

# Check for cross-compilation via _PYTHON_HOST_PLATFORM (e.g., "macosx-10.14-x86_64")
host_platform = os.environ.get('_PYTHON_HOST_PLATFORM', '')
if host_platform:
    print(f"Cross-compile: _PYTHON_HOST_PLATFORM = {host_platform}")
    if 'x86_64' in host_platform:
        machine = 'x86_64'
    elif 'arm64' in host_platform or 'aarch64' in host_platform:
        machine = 'arm64' if 'darwin' in host_platform or 'macos' in host_platform else 'aarch64'
    # Update system if specified
    if 'macos' in host_platform or 'darwin' in host_platform:
        system = 'darwin'
    elif 'linux' in host_platform:
        system = 'linux'

# Normalize machine architecture names
if machine in ['x86_64', 'amd64']:
    machine = 'x86_64'
elif machine in ['aarch64', 'arm64']:
    # Linux uses 'aarch64', macOS uses 'arm64'
    machine = 'aarch64' if system == 'linux' else 'arm64'

if system == 'linux':
    platform_dir = f'linux/{machine}' if machine in ['x86_64', 'aarch64'] else 'linux/x86_64'
elif system == 'darwin':
    platform_dir = f'macos/{machine}' if machine in ['arm64', 'x86_64'] else 'macos/x86_64'
elif system == 'windows':
    platform_dir = 'windows/x64'
else:
    platform_dir = None

print(f"Detected platform: {system} / {machine} -> {platform_dir}")

# Check for bundled libraries first (PyPI install)
bundled_lib_dir = os.path.join(script_dir, 'lib', platform_dir) if platform_dir else None
bundled_include_dir = os.path.join(script_dir, 'include')

# Check if bundled libraries exist by looking for the actual library file
has_bundled_lib = False
if bundled_lib_dir and os.path.exists(bundled_include_dir):
    # Look for library files in the bundled directory
    if os.path.exists(bundled_lib_dir):
        # Check for both libfaest* (Unix) and faest.dll (Windows)
        lib_files = [f for f in os.listdir(bundled_lib_dir) 
                     if (f.startswith('libfaest') and ('.so' in f or '.dylib' in f or f.endswith('.a')))
                     or (f.startswith('faest') and f.endswith('.dll'))]
        has_bundled_lib = len(lib_files) > 0
        if has_bundled_lib:
            print(f"Found bundled library files: {lib_files}")
        else:
            print(f"No library files found in {bundled_lib_dir}")
            print(f"  Directory exists: {os.path.exists(bundled_lib_dir)}")
            print(f"  Contents: {os.listdir(bundled_lib_dir) if os.path.exists(bundled_lib_dir) else 'N/A'}")
    else:
        print(f"Bundled lib directory does not exist: {bundled_lib_dir}")

if has_bundled_lib:
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
    
    # If build directory doesn't exist, try to build from source
    if not os.path.exists(build_dir):
        print(f"FAEST build directory not found: {build_dir}")
        
        if system == 'windows':
            print(f"ERROR: FAEST library not found for Windows", file=sys.stderr)
            print("", file=sys.stderr)
            print("Windows source builds are not supported.", file=sys.stderr)
            print("Please either:", file=sys.stderr)
            print("  1. Use WSL/Linux to install the package", file=sys.stderr)
            print("  2. Install from PyPI which includes pre-built wheels", file=sys.stderr)
            sys.exit(1)
        
        print("Attempting to clone and build faest-ref from GitHub...")
        
        # Determine where to clone faest-ref
        faest_ref_dir = os.path.join(script_dir, '..', 'faest-ref')
        
        if not os.path.exists(faest_ref_dir):
            print(f"Cloning faest-ref repository...")
            try:
                subprocess.run(
                    ['git', 'clone', '--depth=1', 'https://github.com/faest-sign/faest-ref.git', faest_ref_dir],
                    check=True,
                    capture_output=True,
                    text=True
                )
                print(f"✓ Successfully cloned faest-ref to {faest_ref_dir}")
            except subprocess.CalledProcessError as e:
                print(f"ERROR: Failed to clone faest-ref repository", file=sys.stderr)
                print(f"  {e.stderr}", file=sys.stderr)
                sys.exit(1)
            except FileNotFoundError:
                print(f"ERROR: git command not found. Please install git.", file=sys.stderr)
                sys.exit(1)
        
        # Build faest-ref
        build_dir = os.path.join(faest_ref_dir, 'build')
        if not os.path.exists(build_dir):
            print(f"Building FAEST library with meson...")
            
            # Check if meson and ninja are installed, install if missing
            def ensure_build_tool(tool_name):
                """Check if a build tool is available, install via pip if not."""
                try:
                    subprocess.run(
                        [tool_name, '--version'],
                        check=True,
                        capture_output=True,
                        text=True
                    )
                    return True
                except (subprocess.CalledProcessError, FileNotFoundError):
                    print(f"{tool_name} not found, installing via pip...")
                    try:
                        # Use subprocess to install - more reliable than pip.main()
                        result = subprocess.run(
                            [sys.executable, '-m', 'pip', 'install', '--user', tool_name],
                            capture_output=True,
                            text=True
                        )
                        if result.returncode != 0:
                            # Try without --user flag
                            result = subprocess.run(
                                [sys.executable, '-m', 'pip', 'install', tool_name],
                                capture_output=True,
                                text=True
                            )
                        if result.returncode == 0:
                            print(f"✓ Installed {tool_name}")
                            # Add user bin to PATH for the current process
                            user_bin = os.path.expanduser('~/.local/bin')
                            if user_bin not in os.environ.get('PATH', ''):
                                os.environ['PATH'] = user_bin + os.pathsep + os.environ.get('PATH', '')
                            return True
                        else:
                            print(f"ERROR: Failed to install {tool_name}", file=sys.stderr)
                            print(f"  stdout: {result.stdout}", file=sys.stderr)
                            print(f"  stderr: {result.stderr}", file=sys.stderr)
                            return False
                    except Exception as e:
                        print(f"ERROR: Failed to install {tool_name}: {e}", file=sys.stderr)
                        print(f"\nPlease install {tool_name} manually:", file=sys.stderr)
                        print(f"  pip install {tool_name}", file=sys.stderr)
                        return False
            
            if not ensure_build_tool('meson'):
                sys.exit(1)
            if not ensure_build_tool('ninja'):
                sys.exit(1)
            
            # Find meson and ninja executables
            def find_tool(tool_name):
                """Find tool in PATH or common locations."""
                import shutil
                tool_path = shutil.which(tool_name)
                if tool_path:
                    return tool_path
                # Check user local bin
                user_bin = os.path.expanduser(f'~/.local/bin/{tool_name}')
                if os.path.exists(user_bin):
                    return user_bin
                # Check Python Scripts directory (Windows/some setups)
                scripts_dir = os.path.join(os.path.dirname(sys.executable), 'Scripts' if system == 'windows' else '', tool_name)
                if os.path.exists(scripts_dir):
                    return scripts_dir
                return tool_name  # Fallback to just the name
            
            meson_cmd = find_tool('meson')
            ninja_cmd = find_tool('ninja')
            
            try:
                # Run meson setup
                subprocess.run(
                    [meson_cmd, 'setup', 'build'],
                    cwd=faest_ref_dir,
                    check=True,
                    capture_output=True,
                    text=True
                )
                
                # Run ninja (or meson compile)
                try:
                    subprocess.run(
                        [ninja_cmd, '-C', 'build'],
                        cwd=faest_ref_dir,
                        check=True,
                        capture_output=True,
                        text=True
                    )
                except (subprocess.CalledProcessError, FileNotFoundError):
                    # Fallback to meson compile
                    subprocess.run(
                        [meson_cmd, 'compile', '-C', 'build'],
                        cwd=faest_ref_dir,
                        check=True,
                        capture_output=True,
                        text=True
                    )
                
                print(f"✓ Successfully built FAEST library in {build_dir}")
            except subprocess.CalledProcessError as e:
                print(f"ERROR: Failed to build FAEST library", file=sys.stderr)
                print(f"  stdout: {e.stdout}", file=sys.stderr)
                print(f"  stderr: {e.stderr}", file=sys.stderr)
                sys.exit(1)
        
        # Update src_dir to point to faest-ref
        src_dir = faest_ref_dir
    
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
# For runtime library search, we need to handle both bundled (PyPI) and development cases
if has_bundled_lib:
    # For PyPI installs, the libraries will be installed in site-packages/lib/<platform>/
    # The _faest_cffi module will be in site-packages/, so we use $ORIGIN/lib/<platform>
    if system == 'linux':
        runtime_lib_dirs = ['$ORIGIN/lib/' + platform_dir]
    elif system == 'darwin':
        runtime_lib_dirs = ['@loader_path/lib/' + platform_dir]
    else:
        runtime_lib_dirs = None
else:
    # For development, use absolute path
    runtime_lib_dirs = [build_dir] if system in ['linux', 'darwin'] else None

# Handle cross-compilation flags
extra_compile_args = []
extra_link_args = []

# Check ARCHFLAGS for cross-compilation (used on macOS)
archflags = os.environ.get('ARCHFLAGS', '')
if archflags:
    # Parse ARCHFLAGS and add to compile/link args
    extra_compile_args.extend(archflags.split())
    extra_link_args.extend(archflags.split())
    print(f"Cross-compile: Using ARCHFLAGS = {archflags}")

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
    library_dirs=[build_dir],  # Where to find the library at build time
    include_dirs=[build_dir, src_dir],  # Where to find the headers (both build and source)
    runtime_library_dirs=runtime_lib_dirs,  # Set rpath for runtime library search
    extra_compile_args=extra_compile_args if extra_compile_args else None,
    extra_link_args=extra_link_args if extra_link_args else None,
)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
