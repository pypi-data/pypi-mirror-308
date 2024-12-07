#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
import re

from setuptools import setup, find_packages


def install():
    setup(
        name='google_trans_lzx',
        version='0.0.3',
        description='增加可用的代理入参，在构造时传入proxies',
        license='MIT',
        author='SuHun Han',
        author_email='2739638173@qq.com',
        classifiers=['Development Status :: 5 - Production/Stable',
                     'Intended Audience :: Education',
                     'Intended Audience :: End Users/Desktop',
                     'License :: Freeware',
                     'Operating System :: POSIX',
                     'Operating System :: Microsoft :: Windows',
                     'Operating System :: MacOS :: MacOS X',
                     'Topic :: Education',
                     'Programming Language :: Python',
                     'Programming Language :: Python :: 3.6',
                     'Programming Language :: Python :: 3.7',
                     'Programming Language :: Python :: 3.8',
                     'Programming Language :: Python :: 3.9'],
        packages=find_packages(exclude=['tests']),
        keywords='google translate translator',
        install_requires=[
            'httpx==0.24.0',
            'httpx[http2]'
        ],
        python_requires='>=3.6',
        tests_require=[
            'pytest',
            'coveralls',
        ],
        scripts=['translate']
    )


if __name__ == "__main__":
    install()
