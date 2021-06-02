# -*- coding: utf-8 -*-

from collections import OrderedDict

from setuptools import setup, find_packages

import infracalc

with open('README.md') as f:
    readme = f.read()

with open('LICENSE.md') as f:
    license = f.read()

print(find_packages())
setup(
    name=infracalc.__title__,
    version=infracalc.__version__,
    project_urls=OrderedDict((
        ('Documentation', 'https://github.com/cortiz/infra-calc/wiki'),
        ('Code', 'https://github.com/cortiz/infra-calc/wiki'),
        ('Issue tracker', 'https://github.com/cortiz/infra-calc/issues'),
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
        "boto3==1.16.63",
        "botocore==1.19.63",
        "click==7.1.2",
        "colorclass==2.2.0",
        "jmespath==0.10.0",
        "python-dateutil==2.8.1",
        "PyYAML==5.4.1",
        "s3transfer==0.3.4",
        "six==1.15.0",
        "terminaltables==3.1.0",
        "urllib3==1.26.5",
        "XlsxWriter==1.3.7"
    ],
    entry_points={
        'console_scripts': [
            'infracalc=infracalc.cli:cli'
        ]
    }
)
