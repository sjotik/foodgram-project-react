import csv
import json

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Import data from JSON or CSV file'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path', type=str, help='Path to the JSON or CSV file')

    def handle(self, *args, **options):
        file_path = options['file_path']
        if file_path.endswith('.json'):
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
                for item in data:
                    ingredient = Ingredient(
                        name=item['name'],
                        measurement_unit=item['measurement_unit']
                    )
                    ingredient.save()
        elif file_path.endswith('.csv'):
            with open(file_path, 'r') as csv_file:
                reader = csv.reader(csv_file)
                for row in reader:
                    ingredient = Ingredient(
                        name=row[0],
                        measurement_unit=row[1]
                    )
                    ingredient.save()
        else:
            self.stdout.write(self.style.ERROR(
                'Неверный формат файла. Используйте JSON или CSV файл.'))
