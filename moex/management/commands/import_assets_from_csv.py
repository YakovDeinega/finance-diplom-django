import csv
from django.core.management.base import BaseCommand
from moex.models import Asset
from datetime import datetime


class Command(BaseCommand):
    """Импортирует финансовые активы (акции) из файла CSV."""

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']

        with open(csv_file, 'r', encoding='windows-1251') as file:
            reader = csv.DictReader(file, delimiter=',')

            assets_to_be_imported = []
            for row in reader:
                if (
                    row['SUPERTYPE'] == 'Акции'
                    and row['INSTRUMENT_TYPE'] == 'Акция обыкновенная'
                ):
                    registry_date = None

                    if row['REGISTRY_DATE']:
                        try:
                            registry_date = datetime.strptime(row['REGISTRY_DATE'],'%d-%m-%Y').date()
                        except (ValueError, IndexError):
                            pass

                    assets_to_be_imported.append(
                        Asset(
                            isin=row['ISIN'],
                            ticker=row['TRADE_CODE'],
                            name=row['EMITENT_FULL_NAME'],
                            registry_number=row['REGISTRY_NUMBER'],
                            nominal=float(row['NOMINAL'].replace(',', '.')) if row['NOMINAL'] else None,
                            currency=row['CURRENCY'],
                            emitent_inn=row['INN'],
                            emitent_name=row['EMITENT_FULL_NAME'],
                            list_section=row['LIST_SECTION'],
                            registry_date=registry_date,
                        ),
                    )

        Asset.objects.bulk_create(assets_to_be_imported, batch_size=100, ignore_conflicts=True)
