import logging
from core.vk.vk_parser import VKParser
from tatar_analysis.celery import app

# Get an instance of a logger
logger = logging.getLogger(__name__)


@app.task
def update_vk_content():
    parser = VKParser()
    parser.parse_groups()
    logger.info(f'Updated VK groups')
