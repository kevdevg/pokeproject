import time

from celery.utils.log import get_task_logger
from celery import shared_task

from pokemon.api import retrieve_and_create_pokemon
from pokemon.models import Stat

logger = get_task_logger(__name__)


@shared_task
def create_pokemon(name):
    retrieve_and_create_pokemon(name)
    return True