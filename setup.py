from setuptools import setup, find_packages

setup(
    name="car-racing",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pygame",
        "numpy",
    ],
    author="UTN Student",
    author_email="",
    description="A car racing game with genetic AI",
    keywords="pygame, genetic-algorithm, neural-network",
    python_requires=">=3.6",
)
