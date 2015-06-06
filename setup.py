#!/usr/bin/env python
import googletrans
from setuptools import setup, find_packages

def install():
    desc = googletrans.__doc__
    setup(
        name='py-googletrans',
        version='1.1.1',
        description=desc,
        long_description=desc,
        author='SuHun Han',
        author_email='ssut@ssut.me',
        url='https://github.com/ssut/py-googletrans',
        classifiers = ['Development Status :: 5 - Production/Stable',
            'Intended Audience :: Education',
            'Intended Audience :: End Users/Desktop',
            'License :: Freeware',
            'Operating System :: POSIX',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: MacOS :: MacOS X',
            'Topic :: Education',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4'],
        packages=find_packages(),
        install_requires=[
            'requests',
            'future',
        ],
        scripts=['translate'],
    )

if __name__ == "__main__":
    install()