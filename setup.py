#!/usr/bin/env python
'''

  bibparse -- read and write BibTeX files.

  Copyright © 2019 Legisign.org, Tommi Nieminen <software@legisign.org>

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <https://www.gnu.org/licenses/>.

  2019-07-01 setup.py created, packaging underway.
  2019-07-17 BibEntry.update() acquires overwrite=bool parameter.

'''

import setuptools

with open('README.md', 'r') as readme:
    long_description = readme.read()

setuptools.setup(name='bibparse',
                 version='1.1.0',
                 description='Read and write BibTeX files',
                 long_description=long_description,
                 long_description_content_type='text/markdown',
                 url='http://github.com/Legisign/bibparse',
                 author='Legisign.org',
                 author_email='software@legisign.org',
                 license='GPLv3',
                 packages=setuptools.find_packages())
