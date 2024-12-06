import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '0.1.01' #Muy importante, deberéis ir cambiando la versión de vuestra librería según incluyáis nuevas funcionalidades
PACKAGE_NAME = 'pyOSCUD' #Debe coincidir con el nombre de la carpeta 
AUTHOR = 'eduynl'
AUTHOR_EMAIL = 'eduynl@gmail.com'
URL = 'https://github.com/erlopezs/pyOSCUD' #Modificar con vuestros datos

LICENSE = 'GNU General Public License v1.0'
DESCRIPTION = 'Libreria de python para Programacion y Control de Operaciones' #Descripción corta
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8') #Referencia al documento README con una descripción más elaborada
LONG_DESC_TYPE = "text/markdown"


#Paquetes necesarios para que funcione la libreía. Se instalarán a la vez si no lo tuvieras ya instalado
INSTALL_REQUIRES = ['pandas','pulp','numpy','gurobipy','matplotlib','openpyxl','networkx']

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True
)