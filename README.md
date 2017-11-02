# clt_uhcas_auth
This is an extension of Django User model with University of Hawaii CAS authentication attributes based on [edu_uh_cas](https://github.com/songmink/edu_uh_cas) that is modified backends of [django_cas_ng](https://github.com/mingchen/django-cas-ng).

## Getting started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
This is a simple user model extension of django User model with [edu_uh_cas](https://github.com/songmink/edu_uh_cas) backends for Center for Language & Technology of University of Hawaii at Manoa.

### Quick start
1. Install and set up [django_cas_ng](https://github.com/mingchen/django-cas-ng), first.

2. Install from git,
```
pip install git+git://github.com/songmink/edu_uh_cas@master
```

3. Run `python manage.py migrate`

