from django_tenants.utils import get_tenant_domain_model, get_tenant_model
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    CreateTenantSerializer,
    TenantListSerializer,
    TenantSerializer,
    TenantUserSerializer,
)
from .utils import get_tenant_user_model


class TenantListAPIView(ListAPIView):
    """
    Lists all the tenants in the system.
    """

    serializer_class = TenantListSerializer

    def get_queryset(self):
        return get_tenant_model().objects.all()


class TenantAPIView(APIView):
    """
    Get the information of a given tenant.
    Returns the name and the UUID.
    """

    serializer_class = TenantSerializer

    def post(self, request, *args, **kwargs):
        data = request.data or {}
        tenant_name = data.get("tenant_name")

        if tenant_name is None:
            raise ParseError(detail="tenant_name missing.")

        try:
            tenant = get_tenant_model().objects.get(tenant_name__iexact=tenant_name)
        except get_tenant_model().DoesNotExist:
            raise ParseError(detail=f"{tenant_name} does not exist.")

        serializer = self.serializer_class(tenant, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateTenantAPIView(APIView):
    """
    Creates a tenant and corresponding schema.
    """

    serializer_class = CreateTenantSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


class DestroyTenantAPIView(APIView):
    def get_tenant_domains(self, tenant):
        """
        Gets the domains of a tenant.
        """
        return get_tenant_domain_model().objects.filter(tenant=tenant)

    def get_tenant(self, pk):
        try:
            return get_tenant_model().objects.get(pk=pk)
        except get_tenant_model().DoesNotExist:
            raise ParseError(detail=f"Tenant {pk} does not exist.")

    def delete(self, request, pk):
        """
        Deletes a tenant and corresponding domains.
        """
        tenant = self.get_tenant(pk)
        domains = self.get_tenant_domains(tenant)

        try:
            tenant.delete()
            domains.delete()
        except ValueError:
            raise ParseError(detail=str(e))

        return Response(status=status.HTTP_204_NO_CONTENT)


class TenantUserAPIView(APIView):
    """
    Associate a user with a Tenant.
    """

    serializer_class = TenantUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_201_CREATED)


class DestroyTenantUserAPIView(APIView):
    """
    Removes the association of a user and a tenant.
    """

    def get_tenant_user(self, user_id, tenant_id):
        try:
            return get_tenant_user_model().objects.get(pk=tenant_id, user_id=user_id)
        except get_tenant_user_model().DoesNotExist:
            raise ParseError(detail=f"Tenant user does not exist.")

    def delete(self, request, user_id, tenant_id):
        instance = self.get_tenant_user(user_id, tenant_id)
        instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class SetActiveTenantUserAPIView(APIView):
    """
    Sets the current active tenant of a logged in user.
    """

    def get_tenant_user(self, tenant_id):
        try:
            return get_tenant_user_model().objects.get(
                user=self.request.user, tenant_id=tenant_id
            )
        except get_tenant_user_model().DoesNotExist:
            raise ParseError(detail=f"Tenant {tenant_id} for current user not found.")

    def put(self, request, tenant_id, **kwargs):
        instance = self.get_tenant_user(tenant_id)
        instance.is_active = True
        instance.save()

        return Response(status=status.HTTP_200_OK)
