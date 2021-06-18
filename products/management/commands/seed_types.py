from django.core.management.base import BaseCommand
from products.models import ProductType


class Command(BaseCommand):

    help = "This command creates types"

    def handle(self, *args, **options):
        products = [
            "Backend",
            "Frontend",
            "Game",
            "Platform",
            "Machine-Learning",
            "Deep-Learning",
            "BlockChain",
        ]
        for a in products:
            ProductType.objects.create(name=a)

        self.stdout.write(self.style.SUCCESS("types created"))
