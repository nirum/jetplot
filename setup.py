from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import os
import sys
import jetpack

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.md')).read()
except IOError:
    README = ''


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(name='jetpack',
      version=jetpack.__version__,
      author='Niru Maheswaranathan',
      author_email='nirum@stanford.edu',
      url='https://github.com/nirum/jetpack.git',
      requires=[req.strip() for req in open("requirements.txt").readlines()],
      long_description=README,
      packages=find_packages(),
      license='LICENSE.md',
      cmdclass={'test': PyTest}
      )
