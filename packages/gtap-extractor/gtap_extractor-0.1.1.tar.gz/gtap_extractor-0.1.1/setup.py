from setuptools import setup, find_packages

setup(
    name='gtap-extractor',
    version='0.1.1',
    author='Timothe Beaufils',
    author_email='timothe.beaufils@pik-potsdam.de',
    description='Extract GTAP data from .har files and save it as .nc file.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://gitlab.pik-potsdam.de/mrio_toolbox/gtap_extractor',
    packages=find_packages(),
    install_requires=[
        "netcdf4",
        "xarray",
        "mrio_toolbox"
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
    ],
    keywords=[
        'GTAP', 
        'MRIO', 
        "Input-Output", 
        "Economics",
        "Industrial Ecology", 
        "netcdf",
        "International Trade"],
)