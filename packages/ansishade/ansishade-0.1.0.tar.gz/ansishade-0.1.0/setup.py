from setuptools import setup
from ansishade import __version__

VERSION = __version__

setup(
    name="ansishade",
    version=VERSION,
    description="Colored text for terminal",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Kim Yung",
    license="MIT",
    install_requires=[
        'tingetone', 
    ],
    python_requires=">=3.5",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Topic :: Terminals",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
    packages=["ansishade"],
)
