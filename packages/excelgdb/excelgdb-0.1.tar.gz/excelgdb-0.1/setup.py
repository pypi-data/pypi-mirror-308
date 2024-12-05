# from setuptools import setup, find_packages
# setup(
#     name="xlsTogdb",   
#     version="0.1.0",   
#     author="Ali Hasanvand",  
#     author_email="ali.mohamad.hassanvand@gmail.com",  
#     description="A toolkit for converting Excel coordinate to ArcGIS GDB",   
#     long_description=open("README.md").read(),   
#     long_description_content_type="text/markdown",   
#     url="https://github.com/ali-hasanvand",   
#     packages=find_packages(),  
#     install_requires=[
#     ],
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",  
#         "Operating System :: OS Independent",
#     ],
#     python_requires='>=3.6',  
# )

from setuptools import setup, find_packages
setup(
    name="excelgdb",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        
    ],
    author="Hasanvand",
    author_email="ali.mohamad.hassanvand@gmail.com",
    description="A toolkit for converting Excel coordinate to ArcGIS GDB",
    long_description="This package provides tools for working with ArcGIS geometries using arcpy.",
    long_description_content_type="text/markdown",
    url="https://github.com/ali-hasanvand//excelgdb_package",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)