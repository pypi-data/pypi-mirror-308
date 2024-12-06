from setuptools import setup, find_packages

setup(
    name="aegis_framework",
    version="0.1.2",
    author="Metis Analytics",
    author_email="cjohnson@metisos.com",
    description="A modular, extensible AI framework for critical missions",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/metisos/aegis_framework.git",  # Update with your actual URL
    packages=find_packages(),
    install_requires=[
        # List dependencies here
    
        "fuzzywuzzy",
       
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Choose an appropriate license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
