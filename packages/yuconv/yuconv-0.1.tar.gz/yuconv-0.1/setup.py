# -*- coding: utf-8 -*-
#    Copyright (C) 2024  Darko Milosevic

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

from setuptools import setup, find_packages
setup(
    name="yuconv",
    version="0.1",
    author="Darko Milosevic",
    author_email="daremc86@gmail.com",
    url="https://github.com/DarkoMilosevic86/yuconv.git",
    description="YuConv is very simple transliteration tool for Serbian language for Cyrillic2Latin and Latin2Cyrillic transliteration, based on srtools Python package.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        'srtools',
        "python-docx",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
