from setuptools import setup, find_packages

setup(
    name='hcmp-de',
    version='1.0.0',
    author='Rishabh Mehta',
    author_email='Rishabh2.Mehta@ril.com',
    description='Internal Data Engineering utility tool',
    url='https://github.com/fin1te/',
    packages=find_packages(),
    install_requires=[
        'requests',
        'loguru',
        'pycryptodome',
        'setuptools',
        'confluent_kafka'
    ]
)
