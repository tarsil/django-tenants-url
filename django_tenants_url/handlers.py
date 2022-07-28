from django_tenants.utils import get_tenant_domain_model, get_tenant_model

from .utils import get_tenant_user_model


def handle_domain(domain_url, tenant, is_primary):
    """
    Creates/Updates a domain and set the primary.
    """
    domain, _ = get_tenant_domain_model().objects.update_or_create(
        domain=domain_url, tenant=tenant, defaults={"is_primary": is_primary}
    )
    return domain


def handle_tenant(
    domain_url, tenant_name, schema_name, paid_until=None, on_trial=False
):
    """
    Creates/Updates a tenant.
    """
    tenant, _ = get_tenant_model().objects.update_or_create(
        domain_url=domain_url,
        tenant_name=tenant_name,
        schema_name=schema_name,
        defaults={"paid_until": paid_until, "on_trial": on_trial},
    )
    return tenant


def handle_tenant_user(tenant, user, is_active):
    """
    Creates/Updates a tenant.
    """
    tenant_user, _ = get_tenant_user_model().objects.update_or_create(
        tenant=tenant,
        user=user,
        defaults={
            "is_active": is_active,
        },
    )
    return tenant_user
