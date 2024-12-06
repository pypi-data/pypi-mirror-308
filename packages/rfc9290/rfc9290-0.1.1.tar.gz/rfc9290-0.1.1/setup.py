# setup.py
from setuptools import setup, find_packages

setup(
    name="rfc9290",
    version="0.1.1",
    description="Simple encoder/decoder for RFC 9290 Concise Problem Details",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="JAG-UK",
    url="https://github.com/JAG-UK/rfc9290",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "cbor2",
    ],
)
