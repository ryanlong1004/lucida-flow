"""Setup configuration for Lucida Flow."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [
        line.strip() for line in fh if line.strip() and not line.startswith("#")
    ]

setup(
    name="lucida-flow",
    version="1.0.0",
    author="Ryan Long",
    author_email="ryanlong1004@users.noreply.github.com",
    description="CLI tool and API for downloading music from streaming services via Lucida.to",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ryanlong1004/lucida-flow",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Sound/Audio",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "lucida=cli:cli",
        ],
    },
)
