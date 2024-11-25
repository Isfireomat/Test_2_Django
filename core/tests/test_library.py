from typing import Dict, Union, List
from datetime import datetime
from rest_framework.response import Response
from rest_framework.test import APIClient
import pytest
from conftest import client, books

@pytest.mark.django_db
def test_library_books(client: APIClient, 
                       books: List[Dict[str,Union[str, int]]]) -> None:
    for book in books:
        response: Response = client.post('/api/books/',
                                         book,
                                         format='json')
        assert response.status_code == 201
    response: Response = client.get('/api/books/')
    assert response.status_code == 200
    response: Response = client.get('/api/books/1/')
    assert response.status_code == 200
    
    response: Response = client.patch('/api/books/1/')
    assert response.status_code == 200
    start_date: str = "2013-11-25"
    end_date: str = "2019-11-25"
    response: Response = client.post('/api/booklist/',{
                                        "start_date": start_date,
                                        "end_date": end_date
                                        },
                                        format='json')
    assert response.status_code == 200
    date_1: datetime = datetime.strptime(start_date, "%Y-%m-%d").date()
    date_2: datetime = datetime.strptime(end_date, "%Y-%m-%d").date()
    print(response.data)
    for book in response.data['books']:
        assert date_1 <= book['published_date'] and book['published_date'] <= date_2
    new_book: Dict[str, Union[str, int]] = books[0]
    new_book['count_pages'] = 500
    response: Response = client.put('/api/books/1/', 
                                    new_book,
                                    format='json')
    assert response.status_code == 200
    response: Response = client.delete('/api/books/1/')
    assert response.status_code == 204