
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="excelgdb",
    version="0.4",
    packages=find_packages(include=["excelgdb", "excelgdb.*"]),
    include_package_data=True,
    install_requires=[
        
    ],
    author="Hasanvand",
    author_email="ali.mohamad.hassanvand@gmail.com",
    description="A toolkit for converting Excel coordinates to ArcGIS GDB",
    long_description=long_description,   
    long_description_content_type="text/markdown",  
    url="https://github.com/ali-hasanvand/excelgdb.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
