# setup.py
from setuptools import setup, find_packages

setup(
    name="42formatter",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "x42format=42formatter.42formatter:main",
        ],
    },
    author="Antoine Josse",
    author_email="ajosse@student.42.fr",
    description="format input file(s) to 42 norm automatically",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Twatwane/42formatter",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)