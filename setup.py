from setuptools import setup
with open("readme.md",'r', encoding="utf-8") as fh:
    long_description=fh.read()

AUTHOR_NAME='Khushi'
SRC_REPO='src'
LIST_OF_REQUIREMENTS=['streamlit']

setup(
    name=SRC_REPO,
    version='0.01',
    author=AUTHOR_NAME,
    description='A small example package for Movies Reccomendation System',
    long_description=long_description,
    long_description_content_type='text/markdown',
    package=[SRC_REPO],
    python_requires='>=3.7',
    install_requires=LIST_OF_REQUIREMENTS

)