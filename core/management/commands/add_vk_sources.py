import csv
import argparse
import datetime
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

from core.models import VKSource
import logging

logger = logging.getLogger(__name__)

FIELDS_MAPPING = {
    'name': {'name': 'name'},
    'vk_id': {'name': 'vk_id'},
}


def update_sources(data):
    vk_id = data['vk_id']
    try:
        source = VKSource.objects.get(vk_id=vk_id)
        logger.debug(f'Found existing source with id {vk_id}')
    except VKSource.DoesNotExist:
        logger.debug(f'Failed to find existing source with id {vk_id}')
        source = VKSource(vk_id=vk_id)
    for key, value in data.items():
        if key in FIELDS_MAPPING:
            name = FIELDS_MAPPING[key]['name']
            setattr(source, name, value)
    source.save()


class Command(BaseCommand):
    help = 'Loads VK sources from specified CSV file.'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=argparse.FileType('r'))

    def handle(self, *args, **options):
        print('Command load_csv_data started.')
        filename = options['filename']

        reader = csv.DictReader(filename)
        header_row = False
        for row in reader:
            if not header_row:
                try:
                    update_sources(row)
                except IntegrityError as e:
                    logger.warning(f'Failed to load source {row} with error {e}')
            else:
                #  skip header row
                header_row = False
