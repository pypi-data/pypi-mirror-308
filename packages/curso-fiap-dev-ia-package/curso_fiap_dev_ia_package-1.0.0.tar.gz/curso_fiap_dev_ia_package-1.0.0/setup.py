from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='curso_fiap_dev_ia-package',
    version='1.0.0',
    packages=find_packages(),
    description='Descricao da sua lib curso_fiap_dev_ia',
    author='Diogo Leonardo Leal',
    author_email='diogoleal93@gmail.com',
    url='https://github.com/dioleal',  
    license='MIT',  
    long_description=long_description,
    long_description_content_type='text/markdown'
)
