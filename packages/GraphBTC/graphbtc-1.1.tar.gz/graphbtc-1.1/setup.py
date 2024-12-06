"""setup.py for BitcoinPy package. For more details please see BitcoinGraph white paper"""
import setuptools
from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='GraphBTC',
      version='1.1',
      description='Python package containing Bitcoin utilities including blockchain parser, script deciphering, and others',
      author='Mark Bentivegna',
      author_email='markbentivegna@gmail.com',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/markbentivegna/BitcoinPy",
      include_package_data=True,
      packages=setuptools.find_packages(),
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      )
