from setuptools import setup, find_packages

setup(
    name='python2nsp',
    version='1.0',
    description='A simple package that allows Windows computers to communicate to the NSPs. Tailor-made for the BCM-EMU',
    author='Georgios Kokalas',
    packages=['python2nsp'],

    install_requires=['pandas','numpy']
)