from django.conf import settings
from django_tenants.utils import get_tenant_model

try:
    from django.apps import apps

    get_model = apps.get_model
except ImportError:
    from django.db.models.loading import get_model


def get_tenant_user_model():
    return get_model(settings.DTU_TENANT_USER_MODEL)


def get_active_user_tenant(user):
    """
    Obtains the active user tenant.
    """
    from .serializers import TenantSerializer

    try:
        tenant = get_tenant_user_model().objects.get(user=user, is_active=True)
        tenant = tenant.tenant
    except get_tenant_user_model().DoesNotExist:
        return

    serializer = TenantSerializer(tenant)
    return serializer.data


def get_user_tenants(user):
    """
    Lists the tenants associated with a user.
    """
    from .serializers import TenantListSerializer

    tenants = get_tenant_user_model().objects.filter(user=user)
    if not tenants:
        try:
            tenants = [
                get_tenant_model().objects.get(tenant_name=settings.DTU_TENANT_NAME)
            ]
        except get_tenant_model().DoesNotExist:
            return []
    else:
        tenants = [tenant.tenant for tenant in tenants]

    serializer = TenantListSerializer(tenants, many=True)
    return serializer.data


def get_tenants():
    """
    Returns a list of all tenants.
    """
    tenants = get_tenant_model().objects.all()
    serializer = TenantListSerializer(tenants, many=True)
    return serializer.data
