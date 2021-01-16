from django.core.management.base import BaseCommand

from pokemon.api import retrieve_and_create_pokemon


class Command(BaseCommand):
    help = 'Creates a pokemon stored in database'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str)

    def handle(self, **options):
        name = options['name']
        retrieve_and_create_pokemon(name)
