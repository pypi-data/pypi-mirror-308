from setuptools import setup, find_packages

setup(
    name="d5data-http-client",
    version="0.1.24",
    author="Tongzhou Jiang @ d5data.ai",
    author_email="tojiang@d5data.ai",
    description="A simple HTTP client for the d5data API.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/d5data/d5data-http-client",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
