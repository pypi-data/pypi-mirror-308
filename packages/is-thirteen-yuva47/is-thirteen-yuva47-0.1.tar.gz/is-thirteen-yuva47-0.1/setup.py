from setuptools import setup, find_packages

setup(
    name="is-thirteen-yuva47",
    version="0.1",
    author="Yuvaraj",
    author_email="yuvarj68@gmail.com",
    description="A simple package to check if a number is thirteen",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/is-thirteen",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)