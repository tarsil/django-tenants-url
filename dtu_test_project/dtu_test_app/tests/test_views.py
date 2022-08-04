from customers.tests.factories import TenantFactory, TenantUserFactory, UserFactory
from django.contrib.auth import get_user_model
from django.db import IntegrityError, connection
from django.urls import reverse
from django_tenants.test.cases import FastTenantTestCase
from django_tenants.utils import get_tenant_domain_model, get_tenant_model
from django_webtest import WebTest
from dtu_test_app.models import Product

from django_tenants_url.utils import get_tenant_user_model

from .factories import ProductFactory


class BaseTest(FastTenantTestCase):
    def tearDown(self) -> None:
        Product.objects.all().delete()
        connection.set_schema_to_public()
        Product.objects.all().delete()
        get_user_model().objects.all().delete()
        get_tenant_model().objects.all().delete()
        get_tenant_domain_model().objects.all().delete()
        get_tenant_user_model().objects.all().delete()


class TestProductView(BaseTest, WebTest):
    def test_can_access_product_list(self):
        url = reverse("product-list")

        response = self.app.get(url)

        self.assertEqual(200, response.status_code)

    def test_can_access_tenant_data(self):
        user = UserFactory()
        tenant = TenantFactory()
        TenantUserFactory(user=user, tenant=tenant)

        tenant.activate()

        ProductFactory()

        url = reverse("product-tenant-list")

        response = self.app.get(
            url, user=user, headers={"X_REQUEST_ID": str(tenant.tenant_uuid)}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, len(response.json))

    def test_different_result_for_tenant_and_public(self):
        url = reverse("product-tenant-list")
        user = UserFactory()
        tenant = TenantFactory()
        TenantUserFactory(user=user, tenant=tenant)

        tenant.activate()

        for i in range(3):
            ProductFactory()

        response = self.app.get(
            url, user=user, headers={"X_REQUEST_ID": str(tenant.tenant_uuid)}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(3, len(response.json))

        tenant.deactivate()

        for i in range(10):
            ProductFactory()

        response = self.app.get(url, user=user)

        self.assertEqual(10, len(response.json))

    def test_has_no_tenant_permission(self):
        url = reverse("product-tenant-list")
        user = UserFactory()
        tenant = TenantFactory()
        another_tenant = TenantFactory()

        TenantUserFactory(user=user, tenant=tenant)

        tenant.activate()

        for i in range(3):
            ProductFactory()

        response = self.app.get(
            url, user=user, headers={"X_REQUEST_ID": str(tenant.tenant_uuid)}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(3, len(response.json))

        another_tenant.activate()

        for i in range(12):
            ProductFactory()

        total = Product.objects.all()

        self.assertEqual(12, total.count())

        response = self.app.get(
            url,
            user=user,
            headers={"X_REQUEST_ID": str(another_tenant.tenant_uuid)},
            expect_errors=True,
        )

        self.assertEqual(response.status_code, 403)
