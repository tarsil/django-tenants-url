"""
All things middleware
"""
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django_tenants.middleware import TenantMainMiddleware
from django_tenants.utils import (
    get_public_schema_name,
    get_tenant_domain_model,
    get_tenant_model,
)

from .handlers import handle_domain, handle_tenant


class RequestUUIDTenantMiddleware(TenantMainMiddleware):
    """
    Handler of the UUID sent from the request of a user.
    The typical multi-tenant approach would be to split the subdomain
    from the top-level domain but that would also imply handling with those
    configurations via external mapping.

    This middleware does the same job but simply using a UUID sent from the
    header of a request and maps the tenant internally as it was with the subdomain.

    Using `django-tenants` also means using their configurations without
    breaking any existing functionality such as domain creation per tenant and client models.
    """

    def handle_public_domain(self, domain_url, tenant, is_primary):
        """
        Creates an initial public domain in the database.
        """
        return handle_domain(domain_url, tenant, is_primary)

    def handle_public_tenant(
        self, domain_url, tenant_name, schema_name, paid_until, on_trial
    ):
        """
        Creates an initial public tenant.
        """
        return handle_tenant(domain_url, tenant_name, schema_name, paid_until, on_trial)

    def process_request(self, request):
        """
        The connection needs first to be at the public tenant as this is where
        the tenant metadata is stored.
        """
        connection.set_schema_to_public()
        hostname = self.hostname_from_request(request)

        domain_model = get_tenant_domain_model()
        try:
            tenant = self.get_tenant(domain_model, hostname, request)
        except domain_model.DoesNotExist:
            self.no_tenant_found(request, hostname)
            return

        tenant.domain_url = hostname
        request.tenant = tenant
        connection.set_tenant(request.tenant)
        self.setup_url_routing(request)

    def get_tenant(self, model, hostname, request):
        """
        Gets the tenant (public or assigned) from the database.
        If no tenant is found, defaults to public.

        1. Get the domain
        2. Create the schema.
            1. If domain doesn't exist, then creates the schema with the newly assigned domain.
        3. Get the request header.
        4. Return the tenant.
        """
        try:
            domain = model.objects.get(tenant__schema_name=get_public_schema_name())
            schema = domain.tenant
        except ObjectDoesNotExist:
            schema = self.handle_public_tenant(
                domain_url=hostname,
                tenant_name=settings.DTU_TENANT_NAME,
                schema_name=settings.DTU_TENANT_SCHEMA,
                paid_until=settings.DTU_PAID_UNTIL,
                on_trial=settings.DTU_ON_TRIAL,
            )
            self.handle_public_domain(schema.domain_url, schema, True)
        schema.save()

        x_request_id = request.META.get(settings.DTU_HEADER_NAME, schema.tenant_uuid)

        try:
            tenant = get_tenant_model().objects.get(tenant_uuid=x_request_id)
        except get_tenant_domain_model().DoesNotExist:
            tenant = schema

        return tenant
