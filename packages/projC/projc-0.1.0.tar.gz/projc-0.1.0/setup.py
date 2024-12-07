from setuptools import setup, find_packages 


setup(
    name="projC",                      # Nome do projeto
    version="0.1.0",                         # Versão do projeto
    author="Claudia Gabriela",                       # Autor
    author_email="claudiagabriela578@gmail.com",     # Email do autor
    description="Ver clima",
    long_description_content_type="text/markdown",
    url="https://claudiagabriela72.github.io/python/",  # URL do projeto, ex.: GitHub
    packages=find_packages(),                # Encontra pacotes automaticamente
    install_requires=[                       # Dependências do projeto
        "requests",                          # Exemplo de dependência
        "tkinter",
    ],
    classifiers=[                            # Classificações do PyPI
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',                 # Versão mínima do Python
)
