# setup.py

from setuptools import setup, find_packages

setup(
    name="Kam-Ultimate-Reporter",
    version="0.0.5",  # Increment version as needed
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "inquirer>=3.4.0",
        "pandas>=2.2.3",
        "openpyxl>=3.1.5",
        "folioclient>=0.61.1",
        "httpx>=0.27.2",
    ],
    entry_points={
        'console_scripts': [
            'kam-reporter=Kam_Ultimate_Reporter.main:main',  # Use exact package name
        ],
    },
    description="A CLI tool for generating reports from the Kam Ultimate Reporter library system",
    author="Ahmad Awada",
    author_email="ahmed.a.awada@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
