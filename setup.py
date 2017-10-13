import os
import re
from codecs import open
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


def find_version(*file_paths):
    try:
        f = open(os.path.join(here, *file_paths), "r", "utf-8")
        version_file = f.read()
        f.close()
    except:
        raise RuntimeError("Unable to find version string.")

    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name="njaXt",
    version=find_version("njaXt/__init__.py"),
    description="It's not just another XSS tool",
    long_description=long_description,
    url="https://github.com/ujjwal96/njaXt",
    author="Ujjwal Verma",
    author_email="ujjwalverma1111@gmail.com",
    packages=find_packages(include=[
        "njaXt",
        "njaXt.*"
    ]),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "njaxt=njaXt.njaxt:main"
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Environment :: X11 Applications :: Qt",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    install_requires=[
        "pyqt5>=5.9, <5.10"
    ],
    python_requires='>=3.5'
)
