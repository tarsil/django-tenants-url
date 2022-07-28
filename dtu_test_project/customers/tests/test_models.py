from django.contrib.auth import get_user_model
from django.db import IntegrityError, connection
from django.test import TransactionTestCase
from django_tenants.utils import get_tenant_domain_model, get_tenant_model

from django_tenants_url.utils import (
    get_active_user_tenant,
    get_tenant_user_model,
    get_user_tenants,
)

from .factories import TenantFactory, TenantUserFactory, UserFactory


class BaseTest(TransactionTestCase):
    def tearDown(self) -> None:
        connection.set_schema_to_public()
        get_user_model().objects.all().delete()
        get_tenant_model().objects.all().delete()
        get_tenant_domain_model().objects.all().delete()
        get_tenant_user_model().objects.all().delete()


class TestTenantUser(BaseTest):
    def setUp(self) -> None:
        self.user = UserFactory()

    def test_can_create_tenant_user(self):
        tenant = TenantFactory()
        TenantUserFactory(user=self.user, tenant=tenant)

        total = get_tenant_user_model().objects.all()

        self.assertEqual(total.count(), 1)
        self.assertEqual(self.user.tenant_users.count(), 1)

    def test_active_schema_user(self):
        tenant = TenantFactory()
        tenant_user = TenantUserFactory(user=self.user, tenant=tenant, is_active=True)

        self.assertEqual(
            get_active_user_tenant(self.user)["tenant_uuid"],
            str(tenant_user.tenant.tenant_uuid),
        )

    def test_can_be_tenant_of_multiple_customers(self):

        for i in range(3):
            tenant = TenantFactory()
            TenantUserFactory(user=self.user, tenant=tenant)

        self.assertEqual(len(get_user_tenants(self.user)), 3)

    def test_tenant_list(self):

        tenants = []

        for i in range(3):
            tenant = TenantFactory()
            TenantUserFactory(user=self.user, tenant=tenant)
            tenants.append(str(tenant.tenant_uuid))

        user_tenants = sorted(
            [value["tenant_uuid"] for value in get_user_tenants(self.user)]
        )
        tenants = sorted(tenants)

        self.assertEqual(user_tenants, tenants)

    def test_multiple_tenants_one_active(self):
        tenant = TenantFactory()
        TenantUserFactory(user=self.user, tenant=tenant, is_active=True)

        self.assertEqual(
            get_active_user_tenant(self.user)["tenant_uuid"], str(tenant.tenant_uuid)
        )

        tenant_2 = TenantFactory()
        TenantUserFactory(user=self.user, tenant=tenant_2)

        tenant_3 = TenantFactory()
        TenantUserFactory(user=self.user, tenant=tenant_3, is_active=True)

        self.assertEqual(
            get_active_user_tenant(self.user)["tenant_uuid"], str(tenant_3.tenant_uuid)
        )
        self.assertNotEqual(
            get_active_user_tenant(self.user)["tenant_uuid"], str(tenant_2.tenant_uuid)
        )
        self.assertNotEqual(
            get_active_user_tenant(self.user)["tenant_uuid"], str(tenant.tenant_uuid)
        )
