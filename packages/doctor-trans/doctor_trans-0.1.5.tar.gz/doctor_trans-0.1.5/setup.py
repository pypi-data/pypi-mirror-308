# doctor_trans/setup.py

from setuptools import setup, Extension
from Cython.Build import cythonize
import pathlib

# Create the extension for Cython file
ext_modules = [
    Extension(
        name="doctor_trans.trans",
        sources=["doctor_trans/trans.pyx"],  # Path to your .pyx file
    ),
]

# Read the contents of README.md
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")


setup(
    name='doctor_trans',
    version='0.1.5',
    packages=['doctor_trans'],
    ext_modules=cythonize(ext_modules),
    install_requires=[
        'pandas',
        'requests',
        'Cython'
    ],
    author='Nirmal Patel',
    author_email='nirmalpatel1705@gmail.com',
    description='This package translate whole dataframe in any language without any limits.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=''
)
