from setuptools import setup, find_packages

setup(
    name="lotee",
    version="0.1",
    packages=find_packages(),
    install_requires=["requests"],
    author="Safuan P Anvar",
    description="A package to fetch and save a Jupyter Notebook.",
    url="https://github.com/saffuanaanvrr/exam",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
