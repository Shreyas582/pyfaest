"""
Setup script for PyFAEST
"""

import os
import sys
from setuptools import setup, find_packages

# Read the long description from README
readme_file = os.path.join(os.path.dirname(__file__), 'README.md')
if os.path.exists(readme_file):
    with open(readme_file, 'r', encoding='utf-8') as f:
        long_description = f.read()
else:
    long_description = "Python bindings for FAEST post-quantum signature scheme"

setup(
    name='pyfaest',
    version='1.0.4',
    author='PyFAEST Contributors',
    author_email='',
    maintainer='Shreyas Sankpal',
    maintainer_email='shreyas.sankpal@nyu.edu',
    description='Python bindings for FAEST post-quantum digital signature scheme',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Shreyas582/pyfaest',
    project_urls={
        'Bug Tracker': 'https://github.com/Shreyas582/pyfaest/issues',
        'Documentation': 'https://github.com/Shreyas582/pyfaest/tree/main/README.md',
        'Source Code': 'https://github.com/Shreyas582/pyfaest/tree/main/',
    },
    packages=find_packages(exclude=['scripts', 'scripts.*', 'tests', 'tests.*']) + ['lib', 'lib.linux', 'lib.linux.x86_64', 'lib.linux.aarch64', 'lib.macos', 'lib.macos.x86_64', 'lib.macos.arm64', 'lib.windows', 'lib.windows.x64', 'include'],
    package_data={
        'lib.linux.x86_64': ['*.so*'],
        'lib.linux.aarch64': ['*.so*'],
        'lib.macos.x86_64': ['*.dylib'],
        'lib.macos.arm64': ['*.dylib'],
        'lib.windows.x64': ['*.dll'],
        'include': ['*.h'],
    },
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Security :: Cryptography',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: C',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
    ],
    python_requires='>=3.7',
    install_requires=[
        'cffi>=1.15.0',
        'setuptools>=60.0.0',  # Required for Python 3.12+ CFFI compilation
    ],
    setup_requires=[
        'cffi>=1.15.0',
        'setuptools>=60.0.0',
    ],
    cffi_modules=['faest_build.py:ffibuilder'],
    include_package_data=True,
    zip_safe=False,
)
