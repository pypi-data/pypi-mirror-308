from setuptools import setup, find_packages

setup(
    name='pedrusko_operacoes_ifpb2024',                   # Nome do pacote
    version='0.1',                      # Versão inicial
    packages=find_packages(),           # Encontra automaticamente todos os pacotes
    description='Pacote de operações matemáticas básicas',
    author='Pedro Sávio',               # Seu nome
    author_email='pedro.sarmento@academico.ifpb.edu.br', # Seu e-mail
    # url='https://github.com/seuusuario/operacoes', # URL do repositório, caso tenha
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
