from setuptools import setup, find_packages
setup(
name='spottedPy',
version='0.1.1',
author='E. Withnell',
author_email='eloise.withnell.20@ucl.ac.uk',
description='Spatial hotspot analysis',
packages=find_packages(),
download_url='https://github.com/secrierlab/SpottedPy/archive/refs/tags/0.1.1.zip',
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
install_requires=[
        'scanpy',
        'libpysal',
        'esda',
        'numpy',
        'pandas',
        'squidpy',
        'matplotlib',
        'seaborn',
        'tqdm',
        'scikit-learn',
        'statsmodels'],
python_requires='>=3.9',
)