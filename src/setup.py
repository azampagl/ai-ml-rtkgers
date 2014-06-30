#!/usr/bin/env python
"""
Python package setup file.

The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.7
@copyright 2014 - Present Aaron Zampaglione
"""
from distutils.core import setup

setup(
  name='RTKGERS',
  version='1.0',
  description='A hyperplane regression tree learning algorithm.',
  author='Aaron Zampaglione',
  author_email='azampagl@azampagl.com',
  url='http://www.azampagl.com',
  packages=['rtkgers'],
)
