from setuptools import setup, find_packages

setup(
    name="multiroutes",  # Nome do pacote
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "Flask",
    ],
    description="A simple Flask route manager library.",
    author="Seu Nome",
    author_email="seu.email@example.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
