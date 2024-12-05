from setuptools import setup, find_packages
import os

# Utility function to read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

setup(
    name="rifex",
    version="0.0.1",
    description="A CLI tool for video frame interpolation using RIFE",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="dumgum82",
    author_email="dumgum42@example.com",  # Replace with your actual email if desired
    packages=find_packages(),
    include_package_data=True,  # Include non-Python files specified in MANIFEST.in
    package_data={
        "cli": ["ECCV2022-RIFE/**/*"],  # Include all files under ECCV2022-RIFE
    },
    entry_points={
        "console_scripts": [
            "rifex=cli.main:main",
        ],
    },
    install_requires=[
        "ffmpeg-python",
        "Pillow",
        # Add other dependencies here if necessary
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Update if using a different license
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
