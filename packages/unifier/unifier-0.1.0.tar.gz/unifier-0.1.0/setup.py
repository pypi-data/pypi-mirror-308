from setuptools import setup, find_packages

setup(
    name='unifier',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pandas',
    ],
    author='xtech',
    
    python_requires='>=3.6',
)
