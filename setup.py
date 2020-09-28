#!/usr/bin/python3
import io
import os
import sys
import glob
import os.path
import re
from distutils.core import setup

# Package meta-data.
NAME = 'InteractiveHtmlBom'
NAME_PKG = NAME
DESCRIPTION = 'Interactive HTML BOM generation plugin for KiCad'
URL = 'https://github.com/INTI-CMNB/InteractiveHtmlBom/'
EMAIL = 'unknown'
AUTHOR = 'qu1ck'

here = os.path.abspath(os.path.dirname(__file__))
# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
     long_description = '\n' + f.read()

with open("InteractiveHtmlBom/version.py") as f:
    s = f.read()
    m = re.search(r"LAST_TAG = 'v(.*)'", s)
    assert m
    version = m.group(1)

setup(name=NAME,
    version=version,
    description=DESCRIPTION,
    long_description=long_description,
    #long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=[NAME_PKG, NAME_PKG+'/core', NAME_PKG+'/ecad', NAME_PKG+'/ecad/kicad_extra', NAME_PKG+'/dialog'],
    package_dir={NAME_PKG: NAME_PKG},
    package_data={NAME_PKG: ['icon.png','web/*']},
    data_files=[('share/kicad/scripting/plugins/'+NAME_PKG, ['settings_dialog.fbp','__init__.py'])],
    scripts=['InteractiveHtmlBom/generate_interactive_bom.py'],
    #install_requires=['wx'],
    classifiers = ['Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)',
    ],
    platforms   = 'POSIX',
    license     = 'MIT'
)
