#!/usr/bin/env python
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(name = "enaml_opengl",
      version = '0.1',
      description = "OpenGL support for enaml",
      author = "Ulrich Eck",
      author_email = "ulrich.eck@magicvisionlab.com",
      url = "http://www.magicvisionlab.com",
      packages = find_packages('.'),
      package_data = {'enaml_opengl' : ['views/*.enaml']},
      license = "BSD License",
      requires=(
        'pyopengl>=3.1b3',
        'atom>=0.3.9',
        'enaml>=0.9.7',
      ),
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