#!/usr/bin/env python

from setuptools import setup

setup(name='mediaPutter',
      version='2.5.0',
      description='Secure Copy Protocol GUI Wrapper',
      author='Logic.Lighting',
      author_email='putter@logic.lighting',
      options = {'py2exe': {'bundle_files': 1, 'compressed': True, 'includes': ['tkinter','json','pathlib','subprocess','platform','threading','time','re','os']}},
      windows=[{'script':'mediaPutter.py'}],
      zipfile = None,
     )