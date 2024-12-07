from setuptools import setup, find_packages

setup(
    name='folder_structure_generator_7edge-new',
    version='1.0.0',
    description='CLI tool to generate folder structures for services',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/folder-structure-generator-7edge',
    packages=find_packages(),
    install_requires=[
        'InquirerPy'
    ],
    entry_points={
        'console_scripts': [
            'folder-structure-generator=folder_structure_generator.generator:main',
        ],
    },
)
