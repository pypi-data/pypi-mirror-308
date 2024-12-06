from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = 'este paquete le permite formatear cedulas dominicanas'


setup(
      
        name="cedula_do", 
        version=VERSION,
        author="Eduardo Tejada",
        author_email="davidtejadamoreta26@gmail.com",
        description=DESCRIPTION,
        
        packages=find_packages(),
        install_requires=['numpy'], 
        
        keywords=['python', 'cedulas', 'formateo'],
        
)
