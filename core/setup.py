from setuptools import setup,find_packages

__version__ = '1.5'

requirements=open('requirements.txt').readlines()

setup(
    name='PdfWebCore',
    version=__version__,
    author='xcKev',
    author_email='xckevin1620@outlook.com',
    url='https://github.com/Kevin-san/CorePdfPage',
    description='PdfWebCore',
    packages= find_packages(),
    py_modules=['const','deps','entities','readparser','render','spider','test','tools','writecreater'],
    python_requires='>=3.7.0',
    include_package_data = True,
    install_requires=requirements
)