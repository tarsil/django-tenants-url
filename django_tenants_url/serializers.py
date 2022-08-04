import logging
from datetime import datetime

import bleach
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.db.models import Q
from django_tenants.utils import get_tenant_model
from rest_framework import serializers

from .handlers import handle_domain, handle_tenant
from .utils import get_tenant_user_model

logger = logging.getLogger(__name__)


class TenantSerializer(serializers.Serializer):
    """
    Basic tenant information.
    """

    tenant_name = serializers.UUIDField()
    tenant_uuid = serializers.UUIDField()


class TenantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_tenant_model()
        fields = ["id", "tenant_name", "tenant_uuid"]


class CreateTenantSerializer(serializers.Serializer):
    """
    Default serializer for the creation of a tenant.
    """

    tenant_name = serializers.CharField(required=True)
    schema_name = serializers.CharField(required=True)
    domain_url = serializers.CharField(required=True)
    on_trial = serializers.BooleanField(default=False)
    paid_until = serializers.DateField(required=False)
    is_primary = serializers.BooleanField(default=True)

    def _sanitize_field(self, field, value):
        """
        Sanitizes and cleans the data.
        """
        try:
            return bleach.clean(value)
        except (TypeError, ValueError):
            raise serializers.ValidationError(f"Invalid value for {field}.")

    def validate_tenant_name(self, tenant_name):
        return self._sanitize_field("tenant_name", tenant_name)

    def validate_schema_name(self, schema_name):
        schema_name = self._sanitize_field("schema_name", schema_name)
        schema_name = schema_name.replace("-", "_")
        return schema_name.lower()

    def validate_domain_url(self, domain_url):
        domain_url = self._sanitize_field("domain_url", domain_url)
        return domain_url.lower()

    def validate(self, attrs):
        """
        Validates if the tenant is a trial or not and raises error if true and date is missing.

        Make sure that there no duplicate schemas by querying the db and ignoring sensitive cases
        and returning a bool.
        """
        on_trial = attrs["on_trial"]
        paid_until = attrs.get("paid_until", None)

        if not on_trial:
            if not paid_until:
                raise serializers.ValidationError(
                    {"paid_until": "paid_until date is required when on trial."}
                )

            attrs["paid_until"] = settings.DTU_PAID_UNTIL
            return attrs

        if not paid_until:
            raise serializers.ValidationError(
                {"paid_until": "paid_until date is required when on trial."}
            )
        else:
            paid_until = datetime.strptime(paid_until, "%Y-%m-%d")
            now = datetime.utcnow()

            if paid_until < now:
                raise serializers.ValidationError(
                    {"paid_until": "paid_until cannot be before today's date."}
                )

        exists = get_tenant_model().objects.filter(
            Q(schema_name__iexact=attrs["schema_name"])
            | Q(tenant_name__iexact=attrs["tenant_name"])
            | Q(tenant_name__iexact=attrs["domain_url"])
        )

        if exists:
            raise serializers.ValidationError(
                "There is already a tenant with the same name and/or schema."
            )

        return attrs

    def create(self, validated_data):
        """
        Creates a tenant and a domain for that same tenant.
        """
        tenant = handle_tenant(
            domain_url=validated_data["domain_url"].lower(),
            tenant_name=validated_data["tenant_name"],
            schema_name=validated_data["schema_name"],
            on_trial=validated_data["on_trial"],
            paid_until=validated_data["paid_until"],
        )

        handle_domain(tenant.domain_url, tenant, validated_data["is_primary"])


class TenantUserSerializer(serializers.Serializer):
    is_active = serializers.BooleanField(required=True)
    user_id = serializers.IntegerField(required=True)
    tenant_id = serializers.IntegerField(required=True)

    def validate_user_id(self, user_id):
        exists = get_user_model().objects.filter(pk=user_id).exists()
        if not exists:
            raise serializers.ValidationError(
                {"user_id": f"User {user_id} does not exist."}
            )
        return user_id

    def validate_tenant_id(self, tenant_id):
        exists = get_tenant_model().objects.filter(pk=tenant_id).exists()
        if not exists:
            raise serializers.ValidationError(
                {"tenant_id": f"Tenant {tenant_id} does not exist."}
            )
        return tenant_id

    def create(self, validated_data):
        user_id = validated_data["user_id"]
        tenant_id = validated_data["tenant_id"]

        exists = (
            get_tenant_user_model()
            .objects.filter(user_id=user_id, tenant_id=tenant_id)
            .exists()
        )
        if exists:
            raise serializers.ValidationError(
                "There is already a record for this user and tenant."
            )

        try:
            instance = get_tenant_user_model().objects.create(
                user_id=user_id,
                tenant_id=tenant_id,
                is_active=validated_data["is_active"],
            )
        except IntegrityError as e:
            logger.exception(e)
            raise e

        tenants = get_tenant_user_model().objects.all()
        if tenants.count() == 1:
            instance.is_active = True
            instance.save()

        return instance
