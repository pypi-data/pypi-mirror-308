from setuptools import setup, find_packages

setup(
    name="aegis_framework",
    version="0.1.7",
    description="A framework for creating multi-agent colonies",
    author="Metis Analytics",
    author_email="cjohnson@metisos.com",
    url="https://github.com/metisos/aegis_framework.git",
    packages=[
        "aegis_framework",
        "aegis_framework.core",
        "aegis_framework.modules",
        "aegis_framework.utils",
        "aegis_framework.config"  # Added the config package here
    ],
    install_requires=[
        "flask",
        "flask-socketio",
        "fuzzywuzzy",
        "python-socketio",
        "schedule"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
