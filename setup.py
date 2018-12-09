from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='visualastation',
    version='0.1.0',
    description='Another implementation of Last.fm visualization',
    long_description=readme,
    author='Roma Roman',
    author_email='me@protonmail.com',
    url='https://github.com/romaroman/visualastation',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
