from setuptools import setup, find_packages

setup(
    name="clipstack",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pyperclip"
    ],
    entry_points={
        "console_scripts": [
            "clipstack=clipstack.main:main",  # terminal command
        ],
    },
    author="AashutoshDL",
    description="A simple terminal-based clipboard manager in Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AashutoshDL/clipstack",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)