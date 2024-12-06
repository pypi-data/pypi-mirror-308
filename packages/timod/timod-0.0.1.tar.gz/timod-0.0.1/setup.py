# setup.py
from setuptools import setup, find_packages

setup(
    name="timod", 
    version="0.0.1",
    author="Kiord",
    author_email="glenn.kerbiriou@gmail.com",
    description="A PyTorch module wrapper for Taichi kernels",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Kiord/timod", 
    packages=find_packages(),
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