# -*- coding: utf-8 -*-
"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""
# Always prefer setuptools over distutils
from setuptools import setup
from os import path
from glob import glob

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='socio4health',  # Required
    version='0.1.0',  # Required
    description='Socio4health is a Python package for gathering and harmonizing socio-demographic data.',  # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    url='https://github.com/harmonize-tools/socio4health',  # Optional
    author='Diego Irreño, Erick Lozano',  # Optional
    author_email='',  # Optional
    classifiers=[  # Optional
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='extract transform load etl scraping relational census',  # Optional
    package_dir={'': 'src'},  # Optional
    packages=['socio4health', 'socio4health.dto', 'socio4health.enums', 'socio4health.etl', 'socio4health.db', 'socio4health.utils'],  # Required
    python_requires='>=3.7, <4',
    install_requires=['pandas','requests','Scrapy','tqdm', 'pyreadstat', 'py7zr', 'matplotlib', 'numpy'],  # Optional
    extras_require={  # Optional
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    package_data={  # Optional
        'socio4health': ['src/socio4health/config/*.json'],
    },
    data_files=[('harmonize_data', glob('src/socio4health/config/*.json'))],  # Optional
    entry_points={  # Optional
        'console_scripts': [
            'sample=sample:main',
        ],
    },
    project_urls={  # Optional
        'Bug Reports': 'https://github.com//harmonize-tools/socio4health/issues',
        'Source': 'https://github.com//harmonize-tools/socio4health/',
    },
)