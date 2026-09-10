from django.core.management.base import BaseCommand
from finance.models import Category
from finance.seeds.categories import DEFAULT_CATEGORIES

class Command(BaseCommand):
    def handle(self, *args, **options):
        for data in DEFAULT_CATEGORIES:
            Category.objects.get_or_create(name=data["name"], defaults=data)
        self.stdout.write(self.style.SUCCESS("Seed concluído."))
