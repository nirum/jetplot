import os
from setuptools import setup, find_packages

global __version__
__version__ = None

with open('jetplot/version.py') as f:
  exec(f.read(), globals())

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.md')).read()
except IOError:
    README = ''

setup(name='jetplot',
      version=__version__,
      author='Niru Maheswaranathan',
      author_email='niru@hey.com',
      url='https://github.com/nirum/jetplot.git',
      install_requires=['numpy', 'scipy', 'matplotlib'],
      python_requires='>=3.6',
      long_description=README,
      packages=find_packages(),
      license='LICENSE.md'
      )
