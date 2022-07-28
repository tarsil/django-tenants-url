import factory
import factory.django
from django.contrib.auth import get_user_model
from django_tenants.utils import get_tenant_model

from django_tenants_url.utils import get_tenant_user_model


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: "testes-%s" % n)
    password = factory.PostGenerationMethodCall("set_password", "testes")
    first_name = "Test"
    last_name = "User"
    email = factory.LazyAttribute(lambda u: "%s@testes.example.com" % u.username)

    class Meta:
        model = get_user_model()


class TenantFactory(factory.django.DjangoModelFactory):
    tenant_name = factory.Sequence(lambda n: "Tenant - %s" % n)
    schema_name = factory.Sequence(lambda n: "tenant_%s" % n)

    class Meta:
        model = get_tenant_model()


class TenantUserFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    tenant = factory.SubFactory(TenantFactory)

    class Meta:
        model = get_tenant_user_model()
