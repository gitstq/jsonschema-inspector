"""
Setup script for JSONSchema-Inspector
"""

from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="jsonschema-inspector",
    version="1.0.0",
    author="gitstq",
    author_email="",
    description="🔍 Lightweight JSON Schema Visualization & Intelligent Validation Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/jsonschema-inspector",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "jsonschema-inspector=jsonschema_inspector.cli:main",
            "jsi=jsonschema_inspector.cli:main",
        ],
    },
    keywords="json-schema validation visualization mock diff cli",
    project_urls={
        "Bug Reports": "https://github.com/gitstq/jsonschema-inspector/issues",
        "Source": "https://github.com/gitstq/jsonschema-inspector",
    },
)
