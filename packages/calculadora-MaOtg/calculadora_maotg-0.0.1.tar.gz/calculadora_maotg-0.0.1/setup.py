from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="calculadora_MaOtg",
    version="0.0.1",
    author="Mateus O Mendes",
    author_email="ortega.mat@outlook.com",
    description="My short description",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MaOtg/simple-package-template",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)