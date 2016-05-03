from setuptools import setup

setup(
    name='ipython_sparql',
    version='0.1',
    packages=['ipython_sparql'],
    url='https://github.com/baito/ipython_sparql',
    author='Bruno de Oliveira',
    author_email='ddd@dd.com.br',
    description='Jupyter/IPython Extension for Sparql queries',
    license ='MIT',
    keywords='sparql jupyter extension magic ipython',
    install_requires=[
        'ipython',
        'SPARQLWrapper',
        'tabulate'
    ]
)