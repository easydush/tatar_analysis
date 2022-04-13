import logging
from core.vk.vk_parser import VKParser
from parsers.kpfu_parser import download_parse
from tatar_analysis.celery import app

# Get an instance of a logger
logger = logging.getLogger(__name__)


@app.task
def update_vk_content():
    parser = VKParser()
    parser.parse_groups()
    logger.info(f'Updated VK groups')


@app.task
def update_kpfu_content():
    specialitites = ['6343']
    for specialitity in specialitites:
        for year in range(2017, 2021):
            download_parse(specialitity, year)
