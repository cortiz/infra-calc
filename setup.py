# -*- coding: utf-8 -*-

from collections import OrderedDict

from setuptools import setup, find_packages

import infracalc

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

print(find_packages())
setup(
    name=notif.__title__,
    version=notif.__version__,
    project_urls=OrderedDict((
        ('Documentation', 'https://git.rivetlogic.com/projects/RI/repos/notif'),
        ('Code', 'https://git.rivetlogic.com/projects/RI/repos/notif'),
        ('Issue tracker', 'https://issues.rivetlogic.com/projects/IT/issues'),
    )),
    description='Rivet Logic notif tool',
    long_description=readme,
    author='Carlos Ortiz',
    author_email='carlos.ortiz@rivetlogic.com',
    url='https://git.rivetlogic.com/scm/ri/notif.git',
    license=license,
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=[

    ],
    entry_points={

    }
)

