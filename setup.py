# -*- coding: UTF-8 -*-
from setuptools import setup, find_packages
# Nasty hack to make e.g. setup.py register read PKG-INFO as utf-8.. {{{
import sys
reload(sys) # setdefaultencoding is deleted in site.py..
sys.setdefaultencoding('utf-8')
# }}}

setup(
    name = "COURT",
    version = "0.1.0a1",
    description = """An API for crafting organization using resources over time.""",
    long_description = """
    %s""" % "".join(open("README.txt")),
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Database",
        ],
    keywords = "content repository database rdf atom",
    platforms = ["any"],
    author = "Niklas Lindström",
    author_email = "lindstream@gmail.com",
    license = "BSD",
    url = "http://purl.org/court/",
    packages = find_packages(exclude=["test.*", "test"]),
    include_package_data = True,
    zip_safe = False,
    test_suite = 'nose.collector',
    install_requires = [
        'setuptools',
    ],
    #entry_points="""
    #    """,
    )

