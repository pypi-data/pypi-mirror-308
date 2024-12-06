# setup.py
from setuptools import setup, find_packages

setup(
    name='brain-boost', 
    version='0.2.1', 
    packages=find_packages(), 
    description='Librería de ejercicios para mejorar la memoria y agilidad mental',
    author='Elisaruam', 
    author_email='elisa.ruiz@alumni.mondragon.edu',  
    url='https://github.com/Elisaruam/brain-boost.git',  
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  
)
