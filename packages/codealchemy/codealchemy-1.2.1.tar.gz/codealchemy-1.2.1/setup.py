# setup.py
from setuptools import find_packages, setup

setup(
    name="codealchemy",
    version="1.2.1",
    packages=find_packages(),
    install_requires=[
        "confluent-kafka==2.6.0",
        "requests==2.31.0",
        "tabulate==0.9.0",
    ],
    author="GirishCodeAlchemy",
    author_email="girishcodealchemy@gmail.com",
    description="CodeAlchemy is a Python package that provides utility and decorators for development.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/girishcodealchemy/codealchemy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
