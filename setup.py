#!/usr/scripts/env python

from setuptools import setup, find_packages

setup(
    name="pyqt-histogram",
    version="1.0.0",
    packages=find_packages(
        where="lib",
        include="pyqt_histogram/*",
    ),
    package_dir={"": "lib"},
    install_requires=[
        "typer",
        "rich",
        "numpy",
        "matplotlib",
        "pandas",
        "scipy",
        "PyQt6",
        "PyQt6-Charts",
        "pillow",
        "pyyaml",
        "pyqtgraph",
        "PyOpenGL"
    ],
    include_package_data=True,
    entry_points="""
    [console_scripts]
    histo=pyqt_histogram.main:main
    """
)
