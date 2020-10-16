# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""


import re
from setuptools import setup, find_packages

projectName="mkvsubmerge"
scriptFile="%s/%s.py" % (projectName,projectName)
description="Setuptools setup.py for mkvsubmerge."


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open(scriptFile).read(),
    re.M
    ).group(1)


with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")


setup(
    name = projectName,
    packages = find_packages(),
    #add required packages to install_requires list
    install_requires=["pysrt","pymkv"],
    entry_points = {
        "console_scripts": ['%s = %s.%s:main' % (projectName,projectName,projectName)]
        },
    version = version,
    description = description,
    long_description = long_descr,
    long_description_content_type='text/markdown',
    author = "Med0paW",
    author_email = "medopaw@gmail.com",
    url = "https://github.com/medopaw/mkvsubmerge",
    license='MIT',
#list of classifiers: https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=['Development Status :: 3 - Alpha',
 'License :: OSI Approved :: MIT License',
 'Environment :: Console',
 'Natural Language :: English',
 'Operating System :: OS Independent',
 'Programming Language :: Python :: 3',
 'Topic :: Software Development',
 'Topic :: Utilities'],
    )
