#!/usr/bin/python
# -*- coding: utf8 -*-
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

setup(
    name='main',
    version='0.1',
    author='Makina Corpus',
    author_email='geobi@makina-corpus.com',
    url='http://makina-corpus.com',
    description="Webapi GeoNature",
    long_description=open(os.path.join(here, 'README.rst')).read(),
    zip_safe=False,
    install_requires = [
        'django == 1.11.29',  # pinned by buildout
        'psycopg2 == 2.4.1',
        'easydict == 1.4',
        'shapely == 1.2.16',
        'geojson == 1.0.1',
        'simplejson == 2.6.2',        
    ],
    data_files=[('main', ['main/data.db.sample'])],
    tests_requires = [],
    packages=find_packages(),
    classifiers  = ['Natural Language :: English',
                    'Environment :: Web Environment',
                    'Framework :: Django',
                    'Development Status :: 5 - Production/Stable',
                    'Programming Language :: Python :: 2.5'],
)
