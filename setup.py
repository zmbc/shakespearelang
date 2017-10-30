import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="shakespearelang",
    version="0.3.0",
    author="Zeb Burke-Conte",
    author_email="zmbc@uw.edu",
    url='http://github.com/zmbc/shakespearelang',
    description="An interpreter for the Shakespeare Programming Language.",
    license="MIT",
    keywords="shakespeare interpreter",
    packages=['shakespearelang'],
    install_requires=['click', 'grako'],
    long_description=read('README.rst'),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development :: Interpreters",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
        'console_scripts': ['shakespeare=shakespearelang.cli:main'],
    }
)
