from setuptools import setup, find_packages
from config import CONFIGURATION
from utils import PROJ_PATH

with open(PROJ_PATH + 'README.md') as f:
    readme = f.read()

with open(PROJ_PATH + 'LICENSE') as f:
    license = f.read()

setup(
    name=CONFIGURATION.app_name,
    version=CONFIGURATION.app_version,
    description='Another implementation of Last.fm visualization',
    long_description=readme,
    author='romaroman',
    author_email='me@protonmail.com',
    url='https://github.com/romaroman/visulast',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
