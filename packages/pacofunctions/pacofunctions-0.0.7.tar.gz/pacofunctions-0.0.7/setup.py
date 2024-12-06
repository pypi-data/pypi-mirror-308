from setuptools import setup, find_packages

setup(
    name='pacoFunctions',
    version='0.0.7',
    packages=find_packages(),
    include_package_data=True,
    package_data={
         'pacoFunctions': ['data/*'],  # Include all files in the data folder
    },
    url='https://www.pacorush.com.br',
    author='Andre Freire',
    author_email='andre@pacorush.com.br',
    description='Hi'
)
