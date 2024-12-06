# setup.py

from setuptools import setup, find_packages

setup(
    name="aegis_framework",  # Replace with your package name
    version="0.1.4",  # Initial version
    description="A framework for creating multi-agent colonies",
    author="Metis Analytics",  # Replace with your name
    author_email="your_email@example.com",  # Replace with your email
    url="https://github.com/metisos/aegis_framework.git",  # Replace with your URL if available
    packages=find_packages(),
    install_requires=[
        "flask",
        "flask-socketio",
        "fuzzywuzzy",
        "python-socketio",
        "schedule"
    ],  # Add other dependencies as needed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Choose a license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
