from setuptools import setup, find_packages

VERSION = '1.0.0' 
DESCRIPTION = ''
LONG_DESCRIPTION = ''

# Setting up
setup(
       # 'name' deve corresponder ao nome da pasta
        name="BV_VTK_Manager", 
        version=VERSION,
        author="Flavio Pasquetti",
        author_email="<flavio.pasquetti@bureauveritas.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['pandas', 'vtk', 'numpy', 'vtk-module'], 
        keywords=[],
        classifiers= []
)