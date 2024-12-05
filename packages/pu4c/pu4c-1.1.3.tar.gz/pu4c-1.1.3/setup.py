from setuptools import setup, find_packages
import os, sys

cache_dir = '/tmp/pu4c' if (sys.platform.startswith('linux') or sys.platform.startswith('darwin')) else os.path.join(os.environ['TEMP'], 'pu4c')
os.makedirs(cache_dir, exist_ok=True)

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pu4c",
    version="1.1.3",
    packages=find_packages(exclude=["tests"]),
    author="city945",
    author_email="city945@njust.edu.cn",
    url="https://github.com/city945",
    description="A python utils package for city945",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'rpyc',
    ],
)