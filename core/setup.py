from setuptools import setup

__version__ = '2.0'

requirements=open('requirements.txt').readlines()

setup(
    name='PdfWebCore',
    version=__version__,
    author='xcKev',
    author_email='xckevin1620@outlook.com',
    url='https://github.com/Kevin-san/CorePdfPage',
    description='PdfWebCore',
    packages= ['alvinconst','alvindeps','alvinentities','alvinreadparser','alvinrender','alvinspider','alvintest','alvintools','alvinwritecreater'],
    package_dir={'':'core'},
    package_data = {'alvinwritecreater':['*.TTF'],'alvinconst':['*.TTF']},
    python_requires='>=3.7.0',
    include_package_data = True,
    install_requires=requirements
)