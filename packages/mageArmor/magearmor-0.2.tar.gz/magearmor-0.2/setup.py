from setuptools import setup, find_packages

setup(
    name="mageArmor",
    version="0.2",
    author="Rodrigo Correia Santos, Gustavo Santos Rocha",
    author_email="contato.rodrigocorreiaba753@outlook.com.br, contato.gsr13@gmail.com",
    description="Ferramenta de proteção contra prompt injection",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/s2Alive/mageArmor",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
