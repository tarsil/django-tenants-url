from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from . import settings as tenant_settings


class DjangoTenantsUrlConfig(AppConfig):
    name = "django_tenants_url"
    label = "django_tenants_url"
    verbose_name = "Django Tenants URL"

    def ready(self):
        """
        Make sure the default and mandatory values are checked before
        the app is up and running.
        """

        DEFAULT_SETTING_FIELDS = [
            "DTU_TENANT_NAME",
            "DTU_TENANT_SCHEMA",
            "DTU_DOMAIN_NAME",
            "DTU_PAID_UNTIL",
            "DTU_ON_TRIAL",
            "DTU_HEADER_NAME",
            "DTU_AUTO_CREATE_SCHEMA",
            "DTU_AUTO_DROP_SCHEMA",
            "DTU_TENANT_USER_MODEL",
        ]

        # Test for configuration recommendations. These are best practices,
        # they avoid hard to find bugs and unexpected behaviour.
        if not hasattr(settings, "DTU_TENANT_USER_MODEL"):
            raise ImproperlyConfigured("DTU_TENANT_USER_MODEL is not set.")

        # Sets defaults if not declared in the settings
        for value in DEFAULT_SETTING_FIELDS:
            if not hasattr(settings, value):
                setattr(settings, value, getattr(tenant_settings, value))
