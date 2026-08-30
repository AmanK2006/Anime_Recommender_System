from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()
    
setup(
    name="Anime_Recommender",
    author="Aman",
    version="0.2",
    packages= find_packages(),
    install_requires= requirements,
    python_requires=">=3.11"
)