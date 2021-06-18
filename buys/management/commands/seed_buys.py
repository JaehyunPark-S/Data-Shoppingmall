import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from buys import models as buys_models
from users import models as user_models
from products import models as product_models

NAME = "buys"


class Command(BaseCommand):

    help = f"This command creates many {NAME}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help=f"How many {NAME} do you want to create",
        )

    def handle(self, *args, **options):
        number = options.get("number", 1)
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        products = product_models.Product.objects.all()
        seeder.add_entity(
            buys_models.Buy,
            number,
            {
                "status": lambda x: random.choice(["bought"]),
                "buyer": lambda x: random.choice(users),
                "product": lambda x: random.choice(products),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created"))
