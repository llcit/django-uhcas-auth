"""CAS authentication backend"""
from __future__ import absolute_import
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import Group, User
from django.core.exceptions import ImproperlyConfigured

from django_cas_ng.signals import cas_user_authenticated
from django_cas_ng.utils import get_cas_client

from django_cas_ng.backends import CASBackend

import ast

from .models import UHCASUser


class UHCASBackend(CASBackend):
    def authenticate(self, request, ticket, service):
        """Verifies CAS ticket and gets or creates User object"""
        client = get_cas_client(service_url=service)
        username, attributes, pgtiou = client.verify_ticket(ticket)
        if attributes and request:
            request.session['attributes'] = attributes

        if not username:
            return None
        user = None
        username = self.clean_username(username)

        UserModel = get_user_model()

        # Note that this could be accomplished in one try-except clause, but
        # instead we use get_or_create when creating unknown users since it has
        # built-in safeguards for multiple threads.
        if settings.CAS_CREATE_USER:
            user, created = UserModel._default_manager.get_or_create(**{
                UserModel.USERNAME_FIELD: username
            })
            if created:
                user = self.configure_user(user, attributes)
        else:
            created = False
            try:
                user = UserModel._default_manager.get_by_natural_key(username)
            except UserModel.DoesNotExist:
                pass

        if not self.user_can_authenticate(user):
            return None

        if pgtiou and settings.CAS_PROXY_CALLBACK and request:
            request.session['pgtiou'] = pgtiou

        if settings.CAS_APPLY_ATTRIBUTES_TO_USER and attributes:
            # If we are receiving None for any values which cannot be NULL
            # in the User model, set them to an empty string instead.
            # Possibly it would be desirable to let these throw an error
            # and push the responsibility to the CAS provider or remove
            # them from the dictionary entirely instead. Handling these
            # is a little ambiguous.
            user_model_fields = UserModel._meta.fields
            for field in user_model_fields:
                # Handle null -> '' conversions mentioned above
                if not field.null:
                    try:
                        if attributes[field.name] is None:
                            attributes[field.name] = ''
                    except KeyError:
                        continue
                # Coerce boolean strings into true booleans
                if field.get_internal_type() == 'BooleanField':
                    try:
                        boolean_value = attributes[field.name] == 'True'
                        attributes[field.name] = boolean_value
                    except KeyError:
                        continue

            user.__dict__.update(attributes)

            # If we are keeping a local copy of the user model we
            # should save these attributes which have a corresponding
            # instance in the DB.
            if settings.CAS_CREATE_USER:
                user.save()

        # send the `cas_user_authenticated` signal
        cas_user_authenticated.send(
            sender=self,
            user=user,
            created=created,
            attributes=attributes,
            ticket=ticket,
            service=service,
            request=request
        )
        return user

    # ModelBackend has a `user_can_authenticate` method starting from Django
    # 1.10, that only allows active user to log in. For consistency,
    # django-cas-ng will have the same behavior as Django's ModelBackend.
    if not hasattr(ModelBackend, 'user_can_authenticate'):
        def user_can_authenticate(self, user):
            return True

    def clean_username(self, username):
        """
        Performs any cleaning on the "username" prior to using it to get or
        create the user object.  Returns the cleaned username.

        By default, changes the username case according to
        `settings.CAS_FORCE_CHANGE_USERNAME_CASE`.
        """
        username_case = settings.CAS_FORCE_CHANGE_USERNAME_CASE
        if username_case == 'lower':
            username = username.lower()
        elif username_case == 'upper':
            username = username.upper()
        elif username_case is not None:
            raise ImproperlyConfigured(
                "Invalid value for the CAS_FORCE_CHANGE_USERNAME_CASE setting. "
                "Valid values are `'lower'`, `'upper'`, and `None`.")
        return username

    def configure_user(self, user, attributes):
        """
        Configures a user after creation and returns the updated user.

        By default, returns the user unmodified.
        """

        """
        https://www.hawaii.edu/bwiki/display/UHIAM/CAS+Attribute+Release+Policy
        """
        if user:
            u = User.objects.get(username=user)

        if u is not None:
            # basic user model
            if attributes.get('uhEmail'):
                u.email = attributes.get('uhEmail')

            if attributes.get('givenName'):
                u.first_name = attributes.get('givenName')

            if attributes.get('sn'):
                u.last_name = attributes.get('sn')

            u.save()

            # extra user models
            e = UHCASUser(user=u)
            if attributes.get('cn'):
                e.common_name = attributes.get('cn')

            if attributes.get('displayName'):
                e.display_name = attributes('displayName')

            if attributes.get('eduPersonAffiliation'):
                e.affiliation = attributes.get('eduPersonAffiliation')
                for g in e.affiliation:
                    try:
                        g = Group.objects.get(name=g)
                        g.user_set.add(u)
                    except:
                        pass

            if attributes.get('ou'):
                e.department = attributes.get('ou')

            e.save()

        return user
