import os
import uuid

from django.conf import settings
from django.db import models
from django_tenants.models import DomainMixin as TenantDomainMixin
from django_tenants.models import TenantMixin as TenantsMixin

from django_tenants_url.utils import get_tenant_user_model


class TenantMixin(TenantsMixin):
    """
    Model used to map clients (tenants) with the application.
    """

    domain_url = models.URLField(blank=True, null=True, default=os.getenv("DOMAIN"))
    tenant_name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    tenant_uuid = models.UUIDField(default=uuid.uuid4, null=False, blank=False)
    paid_until = models.DateField(null=True, blank=True)
    on_trial = models.BooleanField(null=True, blank=True)
    created_on = models.DateField(auto_now_add=True)

    # Default True, scgema will be automatically created and synched when it is saved.
    auto_create_schema = getattr(settings, "DTU_AUTO_CREATE_SCHEMA", True)
    auto_drop_schema = getattr(settings, "DTU_AUTO_DROP_SCHEMA", False)

    REQUIRED_FIELDS = ("tenant_name", "schema_name")

    class Meta:
        abstract = True

    def delete(self, force_drop=False, *args, **kwargs):
        """
        Drops the tenant schema and prevents dropping the public schema.
        """
        if self.schema_name == settings.DTU_TENANT_SCHEMA:
            raise ValueError("Cannot drop public schema.")

        self._drop_schema(force_drop)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.tenant_name} - {self.created_on}"


class DomainMixin(TenantDomainMixin):
    """
    Model used to map a domain (or many) with a tenant.
    """

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        """
        Deletes a domain and prevents deleting the public domain.
        """
        if (
            self.tenant.schema_name == settings.DTU_TENANT_SCHEMA
            and self.domain == settings.DTU_DOMAIN_NAME
        ):
            raise ValueError("Cannot drop public domain.")
        super().delete(*args, **kwargs)


class TenantUserMixin(models.Model):
    """
    Mapping between user and a client (tenant).
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="tenant_users",
    )
    tenant = models.ForeignKey(
        settings.TENANT_MODEL,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="tenant_users",
    )
    is_active = models.BooleanField(default=False)
    created_on = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.user.pk}, Tenant: {self.tenant}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_active:
            qs = (
                get_tenant_user_model()
                .objects.filter(is_active=True, user=self.user)
                .exclude(pk=self.pk)
            )
            qs.update(is_active=False)
