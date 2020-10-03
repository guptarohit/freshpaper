# !/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys
from shutil import rmtree
from setuptools import setup, Command

# Package meta-data.
NAME = "freshpaper"
DESCRIPTION = "Program to automatically set Bing's `Photo of the day` as your Desktop's wallpaper."
URL = "https://github.com/guptarohit/freshpaper"
AUTHOR = "Rohit Gupta"
VERSION = "1.2.1"

# Packages are required for this module
REQUIRED = ["click", "Pillow"]

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = "\n" + f.read()


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds...")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution...")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

        self.status("Uploading the package to PyPi via Twine...")
        os.system("twine upload dist/*")

        sys.exit()


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    url=URL,
    py_modules=["freshpaper"],
    entry_points={"console_scripts": ["freshpaper=freshpaper:main"]},
    install_requires=REQUIRED,
    include_package_data=True,
    license="BSD",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: BSD License",
    ],
    # $ setup.py publish support.
    cmdclass={"upload": UploadCommand},
)
