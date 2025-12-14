"""Setup configuration for Phyloland Python package."""

from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="phyloland",
    version="0.1.0",
    description="Bayesian phylogeographic inference with competition and dispersal",
    long_description="Python implementation of the Phyloland R package for modeling competition and dispersal in a statistical phylogeographic framework.",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
