from setuptools import setup, find_packages
import os
import jetpack

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.md')).read()
except IOError:
    README = ''

install_requires = [i.strip() for i in open("requirements.txt").readlines()]

setup(name='jetpack',
      version=jetpack.__version__,
      author='Niru Maheswaranathan',
      author_email='nirum@stanford.edu',
      url='https://github.com/nirum/jetpack.git',
      requires=[req.strip() for req in open("requirements.txt").readlines()],
      long_description=README,
      packages=find_packages(),
      license='LICENSE.md'
      )
