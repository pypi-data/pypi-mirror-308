from setuptools import setup, find_packages
import codecs
import os

rootPath = os.path.abspath(os.path.dirname(__file__))

readMePath = os.path.join(rootPath, "README.md")

with codecs.open(readMePath, encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'A simple ORM for Sqlite3'

# Setting up
setup(
    name="dstore-orm",
    version=VERSION,
    author="The Big Engineer (Mutiibwa Grace Peter), Blessing Tukasiima",
    author_email="<dstore.orm.helpdesk@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    url='https://github.com/GracePeterMutiibwa/dstore-orm',
    install_requires=[],
    license='MIT',
    keywords=['python', 'sqlite3', 'orm', 'sqlite3 orm', 'save objects', 'save objects in Python'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.6.0"
)