import os
import re
import setuptools


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def find_version():
    version_file = read("psi/version.py")
    version_re = r"__version__ = '(?P<version>.+)'"
    version = re.match(version_re, version_file).group('version')
    return version


setuptools.setup(
    name="psi",
    version=find_version(),
    description="A Private Set Intersection Library",
    license="Apache-2.0",
    keywords="privacy cryptography",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/OpenMined/PyPSI",
    install_requires=read("requirements.txt").split("\n"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Security :: Cryptography",
    ],
)
