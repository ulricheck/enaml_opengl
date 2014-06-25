#!/usr/bin/env python
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

from distutils.core import setup, Extension
import numpy


setup(name = "enaml_opengl",
      version = '0.1',
      description = "OpenGL support for enaml",
      author = "Ulrich Eck",
      author_email = "ulrich.eck@magicvisionlab.com",
      url = "http://www.magicvisionlab.com",
      packages = find_packages('.'),
      package_data = {'enaml_opengl' : ['views/*.enaml']},
      license = "BSD License",
      requires=[
        'pyopengl',
        'atom',
        'enaml',
      ],
      ext_modules=[Extension('enaml_opengl.external._transformations',
                             ['enaml_opengl/external/transformations.c'],
                             include_dirs=[numpy.get_include()])],
      zip_safe=False,
      long_description = """\
Use OpenGL in enaml applications""",
      classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      )