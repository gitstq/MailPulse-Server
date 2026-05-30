#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MailPulse-Server Setup Configuration
"""

from setuptools import setup, find_packages

setup(
    name="mailpulse-server",
    version="1.0.0",
    author="SOLO Agent",
    author_email="solo-agent@example.com",
    description="Lightweight email server health monitoring and diagnostics CLI tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mailpulse-server",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Communications :: Email",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "dnspython>=2.4.0",
        "rich>=13.0.0",
        "pydantic>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "mailpulse=mailpulse.cli:main",
        ],
    },
)
