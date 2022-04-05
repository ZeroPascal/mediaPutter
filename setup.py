#!/usr/bin/env python

from setuptools import setup
import py2exe, sys
#import tkinter
#from tkinter import tix
#import json
#import pathlib
#import subprocess
#import platform
#import threading
#import time
#import re
#import os

sys.argv.append('py2exe')

setup(name='mediaPutter',
      version='2.2',
      description='Secure Copy Protocol GUI Wrapper',
      author='Logic.Lighting',
      author_email='putter@logic.lighting',
      options = {'py2exe': {'bundle_files': 1, 'compressed': True, 'includes': ['tkinter','json','pathlib','subprocess','platform','threading','time','re','os']}},
     
      windows=[{'script':'mediaPutter.py'}],
      zipfile = None,
     )