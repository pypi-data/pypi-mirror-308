from setuptools import setup, find_packages


setup(
    name='SimAnn',
    version='1',
    description='Simple Simulated Annealing curve fit algorithm',
    author='Giacomo Corucci',
    author_email='giacomocorucci@virgilio.it',
    packages=find_packages(),
    install_requires=['numpy'],
    )
