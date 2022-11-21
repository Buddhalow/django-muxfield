#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


class TestCommand(TestCommand):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from django.conf import settings

        settings.configure(
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                }
            },
            INSTALLED_APPS=(
                'videofield',
            ),
        )

        import django
        from django.test.utils import get_runner

        django.setup()

        TestRunner = get_runner(settings)
        runner = TestRunner(verbosity=1, interactive=False, failfast=False)

        failures = runner.run_tests([])

        if failures > 0:
            sys.exit(1)


setup(
    name='django-muxfield',
    version='0.1.1',
    description='Support for video upload to mux.com in Django models',
    long_description=open('README.rst', 'r').read(),
    author='Alexander Forselius',
    author_email='drsounds@gmail.com',
    url='https://github.com/Buddhalow/django-muxfield',
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Multimedia :: Video',
        'Topic :: Software Development :: Libraries',
    ],
    keywords='django video model field mux.com mp4',
    install_requires=['Django >= 3.1', 'mux_python'],
    tests_require=['Django >= 1.8', 'mux_python'],
    packages=['muxfield'],
    cmdclass={'test': TestCommand}
)