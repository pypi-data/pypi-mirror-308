from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / 'README.md').read_text()

setup(
    name='ec_topsis',
    version='1.0.0',
    license='GNU',
    author='Valdecy Pereira',
    author_email='valdecy.pereira@gmail.com',
    url='https://github.com/Valdecy/ec_topsis',
    packages=find_packages(),
    install_requires=[
        'matplotlib',
        'numpy',
		'pandas',
        'scikit-learn',
        'scipy',
        'seaborn'
    ],
    description='The EC-TOPSIS Method - A Committee Approach for Outranking Problems Using Randoms Weights',
    long_description=long_description,
    long_description_content_type='text/markdown',
)