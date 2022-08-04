from django.conf import settings
from rest_framework.exceptions import NotFound
from rest_framework.permissions import BasePermission

from .utils import get_tenant_user_model


class BaseTenantPermission(BasePermission):
    """
    Simple base permission to handle with tenants with a user.

    If header is not passed, then means public.
    """

    HEADER_NAME = settings.DTU_HEADER_NAME

    def has_tenant(self, request):
        """
        If not header, then tre for public.
        """
        header = request.META.get(self.HEADER_NAME, None)

        if not header:
            return True

        return bool(
            get_tenant_user_model()
            .objects.filter(user=request.user, tenant__tenant_uuid=header)
            .exists()
        )

    def get_tenant_user(self, request):
        header = request.META.get(self.HEADER_NAME, None)

        if not header:
            return True

        try:
            return get_tenant_user_model().objects.get(
                user=request.user, tenant__tenant_uuid=header
            )
        except get_tenant_user_model().DoesNotExist:
            raise NotFound()


class IsTenantAllowedOrPublic(BaseTenantPermission):
    """
    Permission for tenant in a view.
    Verify if there is a tenant uuid passed in the headers.

    True if exists and/or is public. False otherwise.
    """

    def has_permission(self, request, view):
        return self.has_tenant(request)
