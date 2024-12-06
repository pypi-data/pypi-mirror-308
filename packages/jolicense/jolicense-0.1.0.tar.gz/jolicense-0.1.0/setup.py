from setuptools import setup, find_packages

setup(
    name="jolicense",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
        'colorama>=0.4.4',
    ],
    author="Joman21",
    description="A GitHub-based license system",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/oxjoman21/jolicense",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
