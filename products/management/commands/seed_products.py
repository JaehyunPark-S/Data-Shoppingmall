import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from products import models as product_models
from users import models as user_models


class Command(BaseCommand):

    help = "This command creates many products"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="How many products do you want to create",
        )

    def handle(self, *args, **options):
        number = options.get("number", 1)
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        product_type = product_models.ProductType.objects.all()
        product_language = product_models.ProductLanguage.objects.all()
        seeder.add_entity(
            product_models.Product,
            number,
            {
                "name": lambda x: seeder.faker.sentence(),
                "host": lambda x: random.choice(all_users),
                "product_type": lambda x: random.choice(product_type),
                "product_language": lambda x: random.choice(product_language),
                "price": lambda x: random.randint(10000, 500000),
            },
        )
        created_photos = seeder.execute()
        created_clean = flatten(list(created_photos.values()))
        for pk in created_clean:
            product = product_models.Product.objects.get(pk=pk)
            for i in range(5, random.randint(10, 15)):
                product_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    product=product,
                    file=f"product_photos/{random.randint(1, 30)}.webp",
                )
        self.stdout.write(self.style.SUCCESS(f"{number} products created"))
