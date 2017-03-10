# -*- coding: utf-8 -*-
import sys


PY3 = sys.version_info > (3, )

if PY3:
    unicode = str