import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from reviews import models as review_models
from users import models as user_models
from products import models as product_models


class Command(BaseCommand):

    help = "This command creates many reviews"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="How many reviews do you want to create",
        )

    def handle(self, *args, **options):
        number = options.get("number", 1)
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        products = product_models.Product.objects.all()
        seeder.add_entity(
            review_models.Review,
            number,
            {
                "thumbs_up": lambda x: random.randint(1, 5),
                "product": lambda x: random.choice(products),
                "user": lambda x: random.choice(users),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} reviews created"))
