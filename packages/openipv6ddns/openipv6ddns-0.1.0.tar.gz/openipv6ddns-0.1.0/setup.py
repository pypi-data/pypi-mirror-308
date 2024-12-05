from setuptools import setup, find_packages

setup(
    name="openipv6ddns",
    version="0.1.0",
    description="A Python client for OPEN IPv6 DDNS API",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="ne53",
    author_email="neko252222@gmail.com",
    url="https://github.com/ne53/openipv6ddns",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.7",
)
