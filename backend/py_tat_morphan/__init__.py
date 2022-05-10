# -*- coding: UTF-8 -*-
#!/usr/bin/python

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
VERSION_FILE = open(os.path.join(BASE_DIR, 'VERSION'))
__version__ = VERSION_FILE.read().strip()
HFSTOL_VERSION_FILE = open(os.path.join(BASE_DIR, 'TATAR_HFSTOL_VERSION'))
TATAR_HFSTOL_VERSION = VERSION_FILE.read().strip()
