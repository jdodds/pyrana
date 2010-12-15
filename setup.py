#!/usr/bin/env python
import distribute_setup
distribute_setup.use_setuptools()

from setuptools import setup, find_packages

setup(
    name="Pyrana",
    version="1.0.1",
    packages=find_packages(),
    include_package_data=True,
    exclude_package_data={'': ['.gitignore']},
    entry_points = {
        'console_scripts' : [
            'pyrana = Pyrana:main'
        ]
    },
    scripts = ['pyrana/Pyrana.py'],
    setup_requires = ['setuptools_git >= 0.3'],
    zip_safe = False,
    author = "Jeremiah Dodds",
    author_email = "jeremiah.dodds@gmail.com",
    description = "a minimalistic mp3 player",
    long_description=open('README').read(),
    license="LICENSE.txt",
    keywords="music mp3 ogg mp4 musicplayer player",
    url="http://github.com/jdodds/pyrana",
    download_url="http://github.com/jdodds/pyrana/downloads",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: X11 Applications :: GTK',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Topic :: Multimedia',
        'Topic :: Multimedia :: Sound/Audio :: Players',
    ]
)
