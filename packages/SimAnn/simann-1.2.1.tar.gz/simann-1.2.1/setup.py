from setuptools import setup, find_packages


setup(
    name='SimAnn',
    version='1.2.1',
    description='Simple Simulated Annealing curve fit algorithm',
    author='Giacomo Corucci',
    author_email='giacomocorucci@virgilio.it',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/gcorucci/Simple_Simulated_Annealing_curve_fit",
    packages=find_packages(),
    install_requires=['numpy'],
    )
