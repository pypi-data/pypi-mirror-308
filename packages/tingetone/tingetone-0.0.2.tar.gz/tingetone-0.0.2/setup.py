from setuptools import setup
VERSION = '0.0.2'


setup(
    name="tingetone",
    version=VERSION,
    description="ANSI color formatting for output in terminal",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Kim Yung",
    license="MIT",
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
    packages=["tingetone"],
)
