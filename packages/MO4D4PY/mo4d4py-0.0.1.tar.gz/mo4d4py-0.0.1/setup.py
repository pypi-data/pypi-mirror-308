# setup.py

import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.1' # Importante!!! Cambianr la versión de vuestra librería según incluyan nuevas funcionalidades
PACKAGE_NAME = 'MO4D4PY'  # Debe coincidir con el nombre de la carpeta 

AUTHOR = 'Nacho Alvarez' 
AUTHOR_EMAIL = 'joseignacio.alvarez@eviden.com'
URL = 'https://github.com/xxxxxx' 

LICENSE = 'MIT' #Tipo de licencia
DESCRIPTION = 'Paquete para simplificar el uso de la API de MO4D en Python' #Descripción corta
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8') #Referencia al documento README con una descripción más elaborada
LONG_DESC_TYPE = "text/markdown"

#Paquetes necesarios para que funcione la libreía. Se instalarán a la vez si no lo tuvieras ya instalado
INSTALL_REQUIRES = [
      'requests'
      ]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,

    packages=find_packages(),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
   
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    include_package_data=True,
    keywords=['python', 'EVIDEN', 'MO4D4PY'],
    classifiers= [
            "Development Status :: 2 - Pre-Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
