from setuptools import setup, find_packages

setup(
    name="aegis_framework",  # Name of your package (should be unique on PyPI)
    version="0.1.10",  # Version of your package
    description="A framework for creating multi-agent colonies",  # Short description
    author="Metis Analytics",  # Your name or organization
    author_email="cjohnson@metisos.com",  # Your email address
    url="https://github.com/metisos/aegis_framework.git",  # URL for your project
    packages=find_packages(include=["aegis_framework_dev", "aegis_framework.*"]),  # Explicitly find packages under aegis_framework
    install_requires=[
        "flask",
        "flask-socketio",
        "fuzzywuzzy",
        "python-socketio",
        "schedule"
    ],  # List your package's dependencies
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # License for your package
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
