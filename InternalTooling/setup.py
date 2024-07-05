from setuptools import setup, find_packages

setup(
    name='rag_system',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'dspy',
        'sentence-transformers',
        'torch',
        # Add other dependencies
    ],
)
