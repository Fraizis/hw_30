import random

import factory
import factory.fuzzy as fuzzy
from module_30_ci_linters.hw.app.database import db
from module_30_ci_linters.hw.app.models import Client, Parking


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session

    name = factory.Faker("first_name")
    surname = factory.Faker("last_name")
    credit_card = fuzzy.FuzzyText(length=8, chars="123456789")
    car_number = fuzzy.FuzzyText(length=8, chars="123456789")


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session

    address = fuzzy.FuzzyText(prefix="address ")
    opened = fuzzy.FuzzyChoice([True, False])
    count_places = factory.LazyAttribute(lambda x: random.randint(5, 10))
    count_available_places = factory.LazyAttribute(lambda x: random.randint(1, 5))
