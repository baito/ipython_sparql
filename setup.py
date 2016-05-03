from setuptools import setup

setup(
    name='ipython_sparql',
    version='0.1',
    packages=['ipython_sparql'],
    url='',
    author='Bruno de Oliveira',
    author_email='ddd@dd.com.br',
    description='Jupyter/IPython Extension for Sparql queries',
    license ='MIT',
    keywords='sparql jupyter extension magic ipython',
    install_requires=[
        'ipython == 4.2.0',
        'SPARQLWrapper == 1.7.5',
        'tabulate == 0.7.5'
    ]
)