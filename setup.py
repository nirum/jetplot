from setuptools import setup, find_packages
import os
import jetpack

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.md')).read()
except IOError:
    README = ''

setup(name='jetpack',
      version=jetpack.__version__,
      author='Niru Maheswaranathan',
      author_email='nirum@stanford.edu',
      url='https://github.com/nirum/jetpack.git',
      requires=['numpy', 'scipy', 'matplotlib', 'emoji'],
      long_description=README,
      packages=find_packages(),
      license='LICENSE.md'
      )
