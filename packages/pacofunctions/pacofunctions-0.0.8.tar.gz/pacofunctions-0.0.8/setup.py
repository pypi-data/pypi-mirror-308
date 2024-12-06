from setuptools import setup, find_packages

setup(
    name='utilFunctions',
    version='0.0.8',
    packages=find_packages(),
    include_package_data=True,
    package_data={
         'utilFunctions': ['data/*'],  # Include all files in the data folder
    },
    url='https://www.pacorush.com.br',
    author='Andre Freire',
    author_email='andre@pacorush.com.br',
    description='Hi'
)
