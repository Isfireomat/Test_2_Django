from typing import Generator, Dict, List, Union
from django.conf import settings
from django.db import connections
from django.core.management import call_command
from django.db.backends.base.base import BaseDatabaseWrapper
from rest_framework.test import APIClient
import pytest

@pytest.fixture(scope='session', autouse=True)
def celery_eager():
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.CELERY_TASK_EAGER_PROPAGATES = True
    yield
    settings.CELERY_TASK_ALWAYS_EAGER = False
    settings.CELERY_TASK_EAGER_PROPAGATES = False    

@pytest.fixture(scope='session')
def db_setup() -> Generator[BaseDatabaseWrapper, None, None]:
    settings.DATABASES['default']['NAME'] = 'test_db'    
    call_command('migrate', interactive=False)
    yield connections['default']

@pytest.fixture
def client() -> APIClient:
    return APIClient()

@pytest.fixture
def books() -> List[Dict[str,Union[str, int]]]:
    return [
            {
                "title": "Ктулху",
                "author": "Лавкрафт",
                "genre": "Ужасы",
                "count_pages": 30,
                "published_date": "1918-11-25"
            },
            {
                "title": "Metro 2034",
                "author": "Глуховский",
                "genre": "Роман",
                "count_pages": 300,
                "published_date": "2018-11-25"
            },
            {
                "title": "Metro 2033",
                "author": "Глуховский",
                "genre": "Роман",
                "count_pages": 400,
                "published_date": "2014-11-25"
            },
            {
                "title": "Metro 2035",
                "author": "Глуховский",
                "genre": "Роман",
                "count_pages": 530,
                "published_date": "2022-11-25"
            }
            ]