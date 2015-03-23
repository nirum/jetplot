import os
from distutils.core import setup

version = '0.1.0'

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.md')).read()
except IOError:
    README = ''

install_requires = [i.strip() for i in open("requirements.txt").readlines()]

modules = list(map(lambda f: f[:-3],
              filter(lambda f: f.endswith('.py') & ~(f == 'setup.py'),
                     os.listdir('.'))))

setup(name='utils',
      version='0.1.0',
      author='Niru Maheswaranathan',
      author_email='nirum@stanford.edu',
      requires = install_requires,
      license='MIT',
      long_description=README,
      py_modules = modules
 )
