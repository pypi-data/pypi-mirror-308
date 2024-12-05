import os
from setuptools import setup, find_packages

# Function to read requirements from requirements.txt
def parse_requirements(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return f.read().splitlines()
    return []

setup(
    name="CompactObject-TOV",
    version="1.9.8",
    packages=find_packages(),
    install_requires=parse_requirements('requirements.txt'),  # Automatically adds requirements
    # other setup parameters
)