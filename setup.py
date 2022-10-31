import os

from setuptools import find_packages, setup

global __version__
__version__ = None

with open("jetplot/version.py") as f:
    exec(f.read(), globals())

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, "README.md")).read()
except IOError:
    README = ""

setup(
    name="jetplot",
    version=__version__,
    author="Niru Maheswaranathan",
    author_email="niru@hey.com",
    url="https://github.com/nirum/jetplot.git",
    install_requires=["numpy>=1.19", "scipy", "matplotlib"],
    python_requires=">=3.7",
    long_description=README,
    packages=find_packages(),
    license="LICENSE.md",
)
