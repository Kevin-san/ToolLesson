
import os
from setuptools import setup,find_packages

__version__ = '1.0'

requirements=open('requirements.txt').readlines()

setup(
    name='core_pdf_page',
    version=__version__,
    author='xcKev',
    author_email='xckevin1620@outlook.com',
    url='',
    description='core_pdf_page',
    packages= find_packages(exclude=['sql','practices']),
    python_requires='>=3.7.0',
    install_requires=requirements
)