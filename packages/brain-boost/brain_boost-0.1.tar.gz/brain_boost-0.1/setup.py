# setup.py
from setuptools import setup, find_packages

setup(
    name='brain-boost',  # Nombre de tu librería
    version='0.1',  # Versión inicial
    packages=find_packages(),  # Encuentra automáticamente todos los paquetes
    description='Librería de ejercicios para mejorar la memoria y agilidad mental',
    author='Elisaruam',  # Cambia por tu nombre
    author_email='elisa.ruiz@alumni.mondragon.edu',  # Cambia por tu correo
    url='https://github.com/Elisaruam/brain-boost.git',  # Cambia por el enlace a tu repositorio de GitHub
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Versión mínima de Python requerida
)
