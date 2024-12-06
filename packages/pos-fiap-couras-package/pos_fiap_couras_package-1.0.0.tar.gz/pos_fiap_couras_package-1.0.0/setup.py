from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pos_fiap_couras-package',
    version='1.0.0',
    packages=find_packages(),
    description='Descricao da sua lib pos_fiap_couras',
    author='seu nome',
    author_email='seu.email@example.com',
    url='https://github.com/tadrianonet/pos_fiap_couras',  
    license='MIT',  
    long_description=long_description,
    long_description_content_type='text/markdown'
)
