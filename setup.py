from unicodedata import name
from setuptools import find_packages, setup

setup(
    name='mdf2linkml',
    packages=find_packages(include=['mdf2linkml']),
    version='0.0.1',
    description='Converst MDF format to LinkML',
    author='Todd Pihl'
    license'Apache2.0',
    install_requires=['pyyaml'],
    setup_requires=['pytest-runner'],
    tests_requires=['pytest']
    test_suite='tests'
)