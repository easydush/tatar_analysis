import logging
from core.vk.vk_parser import VKParser
from parsers.pdf_loader import download_parse
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
    for year in range(2017, 2020):
        download_parse(9023, year)
