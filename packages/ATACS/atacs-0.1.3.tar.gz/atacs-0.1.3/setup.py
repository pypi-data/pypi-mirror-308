from setuptools import setup, find_packages

setup(
    name='ATACS',
    version='0.1.3',
    author='Chirag Bhatia',
    author_email='chiragbhatia2002@yahoo.com',
    description='A Python package for financial analysis including RSI, MACD, and statistical insights.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'matplotlib',
        'scipy',
        'numpy'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
