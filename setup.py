import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycourselet", # Replace with your own username
    version="0.0.1",
    author="Christoph Laßmann",
    author_email="csharplassi@posteo.de",
    description="Tool to create courselets for Lernsax",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CsharpLassi/pycourselet",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
