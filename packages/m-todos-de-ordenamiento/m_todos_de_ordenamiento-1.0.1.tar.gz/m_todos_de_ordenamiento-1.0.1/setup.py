from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="m_todos_de_ordenamiento",  # Renombrado aquí
    version="1.0.1",
    packages=find_packages(),
    description="Paquete con métodos de ordenamiento en Python",
    author="Victor Eduardo Mendoza Lopez",
    author_email="victormendoza2008@outlook.com",
    url="https://github.com/VictorEML9092/Practica-16.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    long_description=long_description,
    long_description_content_type="text/markdown",
)