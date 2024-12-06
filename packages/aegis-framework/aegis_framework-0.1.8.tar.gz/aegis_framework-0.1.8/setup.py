from setuptools import setup, find_packages

setup(
    name="aegis_framework",  # Name of your package (should be unique on PyPI)
    version="0.1.8",  # Initial version of your package
    description="A framework for creating multi-agent colonies",  # Short description
    author="Metis Analytics",  # Replace with your name
    author_email="cjohnson@metisos.com",  # Replace with your email
    url="https://github.com/metisos/aegis_framework.git",  # Replace with your package's URL
    packages=find_packages(),  # Automatically finds all packages and subpackages
    install_requires=[
        "flask",
        "flask-socketio",
        "fuzzywuzzy",
        "python-socketio",
        "schedule"
    ],  # List your package's dependencies here
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Use your preferred license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
