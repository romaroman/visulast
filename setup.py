from setuptools import setup, find_packages

APP_NAME = 'visulast'
APP_VERSION = '0.1'

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name=APP_NAME,
    version=APP_VERSION,
    description='Another implementation of Last.fm visualization',
    long_description=readme,
    author='romaroman',
    author_email='me@protonmail.com',
    url='https://github.com/romaroman/visulast',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
