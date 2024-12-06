# setup.py
from setuptools import setup, find_packages

from timod import __version__

setup(
    name="timod", 
    version=__version__,
    author="Kiord",
    author_email="glenn.kerbiriou@gmail.com",
    description="A PyTorch module wrapper for Taichi kernels",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Kiord/timod",
    project_urls={
        "Source": "https://github.com/Kiord/timod",
        "Tracker": "https://github.com/Kiord/timod/issues",
    },
    packages=find_packages(include=['timod']),
    install_requires=[
        "torch>=2.0",
        "taichi>=1.6"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)