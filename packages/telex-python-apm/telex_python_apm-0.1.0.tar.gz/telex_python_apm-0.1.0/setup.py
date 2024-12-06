from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="telex_python_apm",
    version="0.1.0",
    description="Telex APM middleware for FastAPI.",
    author="Cyberguru1",
    author_email="hamzacypher34@gmail.com",
    packages=find_packages(),
    install_requires=[
        "fastapi",    
        "httpx",      
        "starlette"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
