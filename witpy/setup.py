from setuptools import find_packages, setup


setup(
    name="witpy",
    packages=find_packages(include=['witpy']),
    version="1.0.1",
    description="witpy is a Python library that contains functions to parse *Wikipedia XML*. The library mainly focuses on extracting data from Revision pages in *JSON* format.",
)
