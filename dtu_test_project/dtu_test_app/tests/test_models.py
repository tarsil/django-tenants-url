from customers.tests.factories import TenantFactory, UserFactory
from django.contrib.auth import get_user_model
from django.db import IntegrityError, connection
from django_tenants.test.cases import FastTenantTestCase
from django_tenants.utils import get_tenant_domain_model, get_tenant_model
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


class TestProductTenant(BaseTest):
    def setUp(self) -> None:
        self.user = UserFactory()

    def test_can_create_product_public_schema(self):
        for i in range(3):
            ProductFactory()

        total_products = Product.objects.all()

        self.assertEqual(3, total_products.count())

    def test_can_create_product_on_different_schemas(self):
        connection.set_schema_to_public()

        ProductFactory()

        test_schema = TenantFactory(schema_name="test_schema", tenant_name="Test")

        total_products = Product.objects.all()

        self.assertEqual(1, total_products.count())

        test_schema.activate()

        ProductFactory()

        total_products = Product.objects.all()

        self.assertEqual(1, total_products.count())
