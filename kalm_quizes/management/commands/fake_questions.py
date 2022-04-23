from django.core.management.base import BaseCommand, CommandError
from kalm_quizes.models import *
from faker import Faker

fake = Faker()


class Command(BaseCommand):
    help = 'Autocreating TextModel'

    def add_arguments(self, parser):
        parser.add_argument('num_of_mods', type=int)

    def handle(self, *args, **options):
        models_set = []
        num = options['num_of_mods']
        for i in range(num):
            model = TextForTest.objects.create(text=fake.paragraph(nb_sentences=2))
            model.save()
            models_set.append(model)

        print(*models_set, sep='\n --')
        return f'Succesfully created {num} models.'
