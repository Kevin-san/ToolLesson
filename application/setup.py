from setuptools import setup,find_packages

__version__ = '1.5'

requirements=open('requirements.txt').readlines()

setup(
    name='PdfWeb',
    version=__version__,
    author='xcKev',
    author_email='xckevin1620@outlook.com',
    url='https://github.com/Kevin-san/CorePdfPage',
    description='PdfWeb',
    packages= find_packages(),
    py_modules=['PdfWeb'],
    python_requires='>=3.7.0',
    include_package_data = True,
    install_requires=requirements
)