from setuptools import setup, find_packages

setup(
    name="at-common-workflow",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "pytest>=8.3.3",
        "pytest-asyncio>=0.24.0",
        "iniconfig>=2.0.0",
        "packaging>=24.2",
        "pluggy>=1.5.0",
    ],
)