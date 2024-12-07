from setuptools import setup, find_packages
from pathlib import Path

# Cargar el contenido del README.md
README = (Path(__file__).parent / "README.md").read_text()

setup(
    name="Movies_and_Series",
    version="0.1.2",
    description="We have created a Series and Movies Library to manage and view information about films and series. This library allows users to organize their collections of movies and series, making it easier to search, analyze ratings, and categorize by genre.",
    author="Grupo_D",
    author_email="ximena.eguskiza@alumni.mondragon.edu",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.3.0"
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "sphinx>=4.0",
            "sphinx_rtd_theme>=0.5"
        ]
    },
    python_requires=">=3.6",
    long_description=README,
    long_description_content_type="text/markdown",
)