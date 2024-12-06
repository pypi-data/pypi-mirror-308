import os
from setuptools import find_packages, setup

install_requires = ['selenium==4.11.2']

setup(
    name='automatedqa',
    version='0.0.1',
    packages=find_packages(),
    install_requires=install_requires,
    include_package_data=True,
    license='BSD License',
    description='Execute specific commands in browser with selenium for QA test.',
    long_description='',
    url='https://github.com/brenokcc',
    author='Breno Silva',
    author_email='brenokcc@yahoo.com.br',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
