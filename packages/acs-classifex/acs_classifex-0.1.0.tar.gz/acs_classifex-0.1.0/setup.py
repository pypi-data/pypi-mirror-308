from setuptools import setup, find_packages

setup(
    name='acs_classifex',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'spacy>=3.0.0',
    ],
    author='ACS',
    author_email='sanketgadge13@gmail.com',
    description='A Python package for training a custom NER model using spaCy',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/godhorus/acs_classifex',  # Your GitHub URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
