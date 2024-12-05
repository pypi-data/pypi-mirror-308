from setuptools import setup, find_packages

setup(
    name="tennflow",
    version="0.1",
    packages=find_packages(),
    install_requires=["requests"],
    author="Your Name",
    description="A package to download Jupyter notebooks from GitHub.",
    url="https://github.com/saffuanaanvrr/exam/blob/main/lab.ipynb",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
