# setup.py
from setuptools import setup, find_packages

setup(
    name="customer_rating_library",
    version="0.1",
    packages=find_packages(),
    description="A library to calculate percentage for the customer ratings.",
    author="Deekshiya",
    author_email="deekshiya19@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
