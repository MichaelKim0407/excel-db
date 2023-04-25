from pathlib import Path

from setuptools import setup, find_packages

from excel_db import __version__

project_dir = Path(__file__).parent

requirements = (
    'openpyxl',
)

requirements_dev_lint = (
    'flake8',
    'flake8-commas',
    'flake8-quotes',
)

requirements_dev_test = (
    'pytest',
    'pytest-cov',
)

requirements_dev = (
    *requirements_dev_lint,
    *requirements_dev_test,
)

setup(
    name='excel-db',
    version=__version__,
    packages=find_packages(exclude=['tests', 'tests.*']),
    description='Model-style Excel File Accessor',
    long_description=(project_dir / 'README.md').read_text(),
    long_description_content_type='text/markdown',

    url='https://github.com/MichaelKim0407/excel-db',
    license='MIT',
    author='Zheng Jin',
    author_email='mkim0407@gmail.com',

    install_requires=requirements,
    extras_require={
        'dev': requirements_dev,
    },

    classifiers=[
        'Intended Audience :: Developers',

        'Development Status :: 3 - Alpha',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',

        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
