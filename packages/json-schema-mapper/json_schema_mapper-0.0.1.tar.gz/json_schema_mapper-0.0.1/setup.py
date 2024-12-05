from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="json_schema_mapper",
    version="0.0.1",
    description="JSON schema mapper",
    author="Abdelrahman Torky",
    author_email="24torky@gmail.com",
    packages=find_packages(),
    install_requires=requirements
)
