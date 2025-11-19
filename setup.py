#!/usr/bin/env python3
"""
Setup script for Live Object Detection
"""

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="live-object-detection",
    version="1.0.0",
    author="Your Name",
    description="Real-time object detection using DETR",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.8",
    install_requires=[
        "opencv-python>=4.5.0",
        "torch>=1.9.0",
        "transformers>=4.20.0",
        "pillow>=8.0.0",
        "numpy>=1.19.0",
    ],
)
