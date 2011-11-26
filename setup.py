#!/usr/bin/env python
'''
Created on Nov 6, 2011

@author: hugosenari
'''
from distutils.core import setup


setup(name='pyoauthgui',
      version='0.9',
      description='Python OAuth auth user interface',
      author='hugosenari',
      author_email='hugosenari@gmail.com',
      url='https://github.com/hugosenari/pyoauthgui',
      packages=('pyoauthgui',),
      requires=('PyWebKitGtk',),
)