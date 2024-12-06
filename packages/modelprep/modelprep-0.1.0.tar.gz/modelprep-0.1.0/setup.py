from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="modelprep",
    version="0.1.0",
    author="Harsh Murari",
    author_email="hmurari@visionify.ai",
    description="A CLI tool for managing and analyzing image datasets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/visionify/modelprep",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "typer>=0.9.0",
        "pillow>=10.0.0",
        "rich>=13.0.0",
    ],
    entry_points={
        "console_scripts": [
            "modelprep=modelprep.cli:app",
        ],
    },
)