#this helps in packaging and distributing the project
#this will help to create local package of the project
#which means we can use us_visa_classifcation_ as a package in other projects
#ex: from us_visa_classifcation_.components import data_ingestion like this bcoz of this tool

from setuptools import setup, find_packages

setup(
    name="us_visa_classifcation",
    version="0.1.0",
    author="akash sharma",
    packages=find_packages() #this will find all the packages in the project
    #find_packages() will look for __init__.py file in the folders and consider them as packages.
)