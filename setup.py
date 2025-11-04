from setuptools import setup, find_packages

setup(
    name="custom-clipboard",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pyperclip"
    ],
    entry_points={
        "console_scripts": [
            "clipman=custom-clipboard.main:main",  # terminal command
        ],
    },
    author="AashutoshDL",
    description="A simple terminal-based clipboard manager in Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AashutoshDL/custom-clipboard",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
