#!/usr/bin/env python3

from setuptools import setup
import distutils
from distutils.command.install_lib import install_lib
import os
import sys



# We store our version number in a simple text file:
version_path = os.path.join(
    os.path.dirname(__file__),
    'uparma', 'version.txt'
)
with open(version_path, 'r') as version_file:
    uparma_py_version = version_file.read().strip()


setup(
    name='uparma',
    version = uparma_py_version,
    packages = ['uparma'],
    package_dir = {'uparma': 'uparma'},
    description='uparma',
    package_data = {
        'uparma' : [
            'version.txt',
        ]
    },
    long_description = 'Universal Parameter Mapper for Proteomics tools',
    author = '... and Christian Fufezan',
    author_email = 'christian@fufezan.net',
    url = 'http://github.com/uparma/uparma-py',
    license = 'Lesser GNU General Public License (LGPL)',
    platforms = 'any that supports python 3.4',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: SunOS/Solaris',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)

