# coding=utf-8
import setuptools
from AnaviInfraredPhat import __version__

with open("README.md") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AnaviInfraredPhat",
    version=__version__,
    author="KurisuD",
    author_email="KurisuD@pypi.darnand.net",
    description="AnaviInfraredPhat",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KurisuD/AnaviInfraredPhat",
    packages=setuptools.find_packages(),
    install_requires=['pigpio', 'pyzmq', 'pap_logger'],
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "License :: Public Domain",
        "Operating System :: POSIX :: Linux",
        "Topic :: Home Automation"
    ],
)
