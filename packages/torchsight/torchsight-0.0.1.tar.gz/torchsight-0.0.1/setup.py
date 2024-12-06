from setuptools import setup, find_packages

VERSION = "0.0.1"

NAME = "torchsight"

INSTALL_REQUIRES = ["torch"]


setup(
    name=NAME,
    version=VERSION,
    description="Tools for profiling, visualizing and reducing memory overhead while training model wth Pytorch.",
    url="https://github.com/Ben-Schneider-code/TorchSight",
    project_urls={
        "Source Code": "https://github.com/Ben-Schneider-code/TorchSight",
    },
    author="Benjamin Schneider",
    author_email="benjamin.schneider@uwaterloo.ca",
    license="MIT",
    python_requires=">=3.10",
    install_requires=INSTALL_REQUIRES,
    package_dir={"": "src"},
    packages=find_packages("src"),
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
)