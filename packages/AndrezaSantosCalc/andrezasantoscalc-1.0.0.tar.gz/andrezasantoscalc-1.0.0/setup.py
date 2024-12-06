from setuptools import setup, find_packages

setup(
    name="AndrezaSantosCalc",
    version="1.0.0",
    author="Andreza Santos",
    description="Uma biblioteca para realizar operações básicas de uma calculadora.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
