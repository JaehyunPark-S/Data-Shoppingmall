from django.core.management.base import BaseCommand
from products.models import ProductLanguage


class Command(BaseCommand):

    help = "This command creates languages"

    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         "--times",
    #         help="How many thimes do you want me to tell you that I love you?",
    #     )

    def handle(self, *args, **options):
        products = [
            "C",
            "C#",
            "C++",
            "Go",
            "Java",
            "JavaScript",
            "Kotlin",
            "PHP",
            "Python",
            "R",
            "Ruby",
            "Rust",
            "Scala",
            "Swift",
            "Objective-C",
        ]
        for a in products:
            ProductLanguage.objects.create(name=a)

        self.stdout.write(self.style.SUCCESS("Languages created"))
