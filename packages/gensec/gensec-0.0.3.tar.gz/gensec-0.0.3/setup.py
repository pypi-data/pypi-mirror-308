from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gensec",
    version="0.0.3",
    packages=find_packages(),
    include_package_data=True,
    description="A Python package for generating secure docker and k8s resources",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "click", 
        "InquirerPy",
    ],
    entry_points={
        "console_scripts": [
            "gensec=gensec.main:main",
        ],
    },
)
