
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="helpdb",
    version="0.1.0",
    author="Ваше Имя",
    author_email="ваш.email@example.com",
    description="Простая в использовании библиотека для работы с SQLite",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ваш_username/helpdb",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
