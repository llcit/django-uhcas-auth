import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='uhcas_auth',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    descsription='A simple uh cas authentication.',
    long_description=README,
    url='https://github.com/llcit/django-uhcas-auth,
    author='Song M Kim',
    author_email='songmink@hawaii.edu',
    install_requires=[
        'django-cas-ng',
    ],
    zip_safe = False,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: python :: 2'
        'Programming Language :: python :: 2.7'
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ]
)
