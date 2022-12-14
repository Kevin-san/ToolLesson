
import os
from setuptools import setup,find_packages

__version__ = '1.2'

requirements=open('requirements.txt').readlines()

setup(
    name='core_pdf_page',
    version=__version__,
    author='xcKev',
    author_email='xckevin1620@outlook.com',
    url='https://github.com/Kevin-san/CorePdfPage',
    description='core_pdf_page',
    packages= find_packages(exclude=['sql','practices']),
    py_modules=["PdfWeb","const","deps","entities","readparser","render","spider","test","tools","writecreater"],
    package_dir= {'application':'core_pdf_page/application',
                  'core':'core_pdf_page/core',
                  'static':'core_pdf_page/static',
                  'templates':'core_pdf_page/templates'
                  },
    python_requires='>=3.7.0',
    include_package_data = True,
    install_requires=requirements
)