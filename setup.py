#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import join as join_path
from os.path import dirname
from setuptools import find_packages
from setuptools import setup


def _read(file_name):
    sock = open(file_name)
    text = sock.read()
    sock.close()
    return text

setup(
    name = 'pyramid_redis',
    version = '0.2.0+5c7c17ad0bc348e9bc8c934139ca8a3f12d7cb59',
    description = 'Integrate redis with a Pyramid application.',
    author = 'James Arthur',
    author_email = 'username: thruflo, domain: gmail.com',
    url = 'http://github.com/thruflo/pyramid_redis',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Framework :: Pylons',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    license = _read('UNLICENSE').split('\n')[0],
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data = True,
    zip_safe = False,
    install_requires=[
        'redis>=2.10.0',
    ],
    extras_require={
        'test': [
            'pytest'
        ],
        'develop': [
            'fakeredis'
        ],
    }
)
