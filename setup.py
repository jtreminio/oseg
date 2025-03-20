from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")
VERSION = "0.2-dev"

setup(
    name="oseg",
    version=VERSION,
    description="OpenAPI SDK Example Generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jtreminio/oseg",
    author="Juan Treminio",
    author_email="jtreminio@gmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
    ],
    keywords="OpenAPI, openapi-generator, sdk",
    packages=find_packages(where=""),
    python_requires=">=3.12",
    install_requires=[
        "black~=25.0",
        "Jinja2~=3.1",
        "openapi-pydantic~=0.5",
        "pydantic~=2.10",
        "PyYAML~=6.0",
        "click~=8.1",
        "tabulate~=0.9",
        "setuptools~=76.0",
    ],
    extras_require={
        "dev": [
            "coverage~=7.6",
            "mock~=5.2",
        ],
        "test": [],
    },
    entry_points={
        "console_scripts": [
            "run=run:cli",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/jtreminio/oseg/issues",
        "Source": "https://github.com/jtreminio/oseg",
    },
)
