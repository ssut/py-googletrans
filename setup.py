#!/usr/bin/env python
import googletrans
import os.path
from setuptools import setup, find_packages


def readme():
    path = os.path.join(os.path.dirname(__file__), 'README.rst')
    try:
        with open(path) as f:
            return f.read()
    except IOError:
        pass


def install():
    setup(
        name='googletrans',
        version=googletrans.__version__,
        description=googletrans.__doc__,
        long_description=readme(),
        license='MIT',
        author='SuHun Han',
        author_email='ssut' '@' 'ssut.me',
        url='https://github.com/ssut/py-googletrans',
        classifiers=['Development Status :: 5 - Production/Stable',
                     'Intended Audience :: Education',
                     'Intended Audience :: End Users/Desktop',
                     'License :: Freeware',
                     'Operating System :: POSIX',
                     'Operating System :: Microsoft :: Windows',
                     'Operating System :: MacOS :: MacOS X',
                     'Topic :: Education',
                     'Programming Language :: Python',
                     'Programming Language :: Python :: 2.7',
                     'Programming Language :: Python :: 3.4',
                     'Programming Language :: Python :: 3.5',
                     'Programming Language :: Python :: 3.6'],
        packages=find_packages(exclude=['docs', 'tests']),
        keywords='google translate translator',
        install_requires=[
            'requests',
        ],
        extras_require={
            'h2': ['hyper'],
        },
        tests_require=[
            'pytest',
            'coveralls',
        ],
        scripts=['translate']
    )


if __name__ == "__main__":
    install()
