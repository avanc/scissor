#!/usr/bin/env python

from distutils.core import setup

import sys
sys.path.append('src/')
from scissor.version import __version__


setup(name='scissor',
      version=__version__,
      description='Tool to decode and cut otrkey movies.',
      author='Sven Klomp',
      author_email='mail@klomp.eu',
      url='http://none',
      packages=['scissor', 'scissor.cut', 'scissor.move', 'scissor.otr'],
      package_dir={'scissor': 'src/scissor'},
      scripts=['src/scissor.py']
     )

