import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vodacompay",
    version="3.1.0",
    author="Tralah M Brian",
    author_email="briantralah@gmail.com",
    description="A library to interface with vodacom's Payment System using an intermediary server.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TralahM/vodacompay",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "certifi",
        "chardet",
        "future",
        "idna",
        "requests",
        "six",
        "urllib3",
        "pytest",
        "lxml",
    ],
)
