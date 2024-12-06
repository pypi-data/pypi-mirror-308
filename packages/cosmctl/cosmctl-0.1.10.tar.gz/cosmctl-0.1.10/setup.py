from setuptools import setup, find_packages

setup(
    name='cosmctl',
    version='0.1.10',
    author='COSM DevOps',
    author_email='373265@niuitmo.ru',
    description='CLI tool for deploying cosm lab projects',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'cosmctl=cosmctl.main:main',
        ],
    },
)
