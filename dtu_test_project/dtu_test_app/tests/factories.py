import factory
import factory.django
from dtu_test_app.models import Product


class ProductFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: "Product -%s" % n)

    class Meta:
        model = Product
