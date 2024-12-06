# setup.py

from setuptools import setup, find_packages

setup(
    name="Kam-Ultimate-Reporter",
    version="0.0.2",  # Increment the version as needed
    packages=find_packages(),
    install_requires=[
        "inquirer>=3.4.0",       # For CLI prompts
        "pandas>=2.2.3",         # For data manipulation
        "openpyxl>=3.1.5",       # For Excel handling with pandas
        "folioclient>=0.61.1",   # If your project uses FOLIO integration
        "httpx>=0.27.2",         # For making HTTP requests if used in your code
    ],
    entry_points={
        'console_scripts': [
            'kam-reporter=kam_ultimate_reporter.main:main',  # Command name and entry point
        ],
    },
    description="A CLI tool for generating reports from the Kam Ultimate Reporter library system",
    author="ahmad awada",
    author_email="ahmed.a.awada@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
