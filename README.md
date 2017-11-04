# clt_uhcas_auth
[![Python](https://img.shields.io/badge/python-2.7,3.4,3.5,3.6-blue.svg?style=flat)](https://www.python.org)
[![Django](https://img.shields.io/badge/django-1.8,1.9,1.10-green.svg?style=flat)](https://www.djangoproject.com)

This is an extension of Django User model with University of Hawaii CAS authentication attributes based on [edu_uh_cas](https://github.com/songmink/edu_uh_cas) that is modified backends of [django_cas_ng](https://github.com/mingchen/django-cas-ng).

## Getting started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
This is a simple user model extension of django User model with [edu_uh_cas](https://github.com/songmink/edu_uh_cas) backends for Center for Language & Technology of University of Hawaii at Manoa.

### Quick start
1. Install [django_cas_ng](https://github.com/mingchen/django-cas-ng).
2. Set up your settings with [django_cas_ng](https://github.com/mingchen/django-cas-ng).
3. Download `uhcas_auth` on your django project.
4. Add your settings `uhcas_auth`.
```python
INSTALLED_APPS = (
	...
	'<your app directory>.uhcas_auth',
	...
)
```
5. Migrate your database,
```bash
python manage.py migrate uhcas_auth
```
