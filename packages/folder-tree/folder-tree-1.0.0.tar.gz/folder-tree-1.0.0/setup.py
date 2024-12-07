from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()
setup(
    name='folder-tree',
    version='1.0.0',
    description='A package to display folder structures in a tree format',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Sanosh',
    packages=find_packages(),  
    entry_points={
        'console_scripts': [
            'folder-tree=folder_tree.tree:main', 
        ],
    },
    python_requires='>=3.6',
)