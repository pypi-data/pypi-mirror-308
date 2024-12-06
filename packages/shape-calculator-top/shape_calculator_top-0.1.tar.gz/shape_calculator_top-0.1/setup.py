from setuptools import setup, find_packages

setup(
    name="shape_calculator_top",
    version="0.1",
    description="A simple package to calculate areas of different shapes",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Shree Ram",
    author_email="mekashreeram@gmail.com",
    url="https://github.com/mshreeram/shape_calculator",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
