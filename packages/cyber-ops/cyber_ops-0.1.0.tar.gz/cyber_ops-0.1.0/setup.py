from setuptools import setup, find_packages

setup(
    name="cyber_ops",
    version="0.1.0",
    packages=find_packages(),
    description="Cyberops toolkit",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Cyber Whiz",
    author_email="cyberwhizy@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)