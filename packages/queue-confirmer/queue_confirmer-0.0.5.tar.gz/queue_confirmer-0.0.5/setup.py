from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

VERSION = '0.0.5'
DESCRIPTION = 'Handling server and client information'
LONG_DESCRIPTION = 'A package that allows you to handle server and client interaction.'

setup(
    name="queue_confirmer",
    version=VERSION,
    author="MichaeCarlsonDev (Michael Carlson)",
    author_email="<soprano19522@gmail.com>",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'sockets', 'solar car', 'threading'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
