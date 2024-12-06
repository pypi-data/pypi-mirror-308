# setup.py
from setuptools import setup, find_packages

setup(
    name="mati_pkg",
    version="0.1",
    packages=find_packages(),
    install_requires=[],  # Add dependencies here
    entry_points={
        'console_scripts': [
            'my_package_greet=my_package.main:greet',  # command-line tool
        ],
    },
    author="mati",
    description="A simple greeting package",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
