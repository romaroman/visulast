from setuptools import setup, find_packages
from config import Configuration
from visulast.utils.helpers import PROJ_PATH

with open(PROJ_PATH + 'README.md') as f:
    readme = f.read()

with open(PROJ_PATH + 'LICENSE') as f:
    license = f.read()

setup(
    name=Configuration().app_name,
    version=Configuration().app_version,
    description='Telegram bot which visualize your last.fm library',
    long_description=readme,
    author='romaroman',
    author_email='chaban.roman@protonmail.com',
    url='https://github.com/romaroman/visulast',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
