# -*- coding: utf-8 -*-

import codecs
import os
from setuptools import setup, find_packages


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


# read requirements
fname = os.path.join(os.path.dirname(__file__), 'requirements.txt')
with open(fname) as f:
    requirements = [l.strip() for l in f.readlines()]

setup(
    name='warning_service',
    version=1,
    packages=find_packages(),
    package_data={
        '': ['alembic.ini', 'config.yml'],
        'warning_service': ['public/*', 'public/*/*', 'public/*/*/*', 'alembic/versions/*', 'alembic/*'],
        'warning_service.db': ['fixtures.json']
    },
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'warning-service = warning_service.run:main'
        ],
    },
    author='Anton Lavrov',
    author_email='mr.antlav@gmail.com',
    description='Warning Service',
    url='https://github.com/penguinlav/warning-service',
    license="MIT",
)
