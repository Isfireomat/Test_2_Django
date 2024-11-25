from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer, BookListSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F, Window
from django.db.models.functions import Rank
from drf_spectacular.utils import extend_schema

@extend_schema(
    summary="CRUD книги",
    description="Эндпоинт для CRUD книг.",
    request=BookSerializer, 
    tags=["Книги"], 
)
class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['author', 'genre']  
    search_fields = ['title', 'description'] 
    ordering_fields = ['title', 'count_pages', 'published_date']  
    ordering = ['count_pages']  

@extend_schema(
    summary="Получение списка книг с ранжированием",
    description="Эндпоинт для получение списка книг с ранжированием.",
    request=BookListSerializer, 
    tags=["Книги"], 
)
class BookList(APIView):
    serializer_class = BookListSerializer
    def post(self, request):
        serializer: BookListSerializer = BookListSerializer(data=request.data)
        if not serializer.is_valid(): 
            return Response({'message': 'Error with serializer'},
                            status=status.HTTP_400_BAD_REQUEST)
        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']
        try:
            books = Book.objects.filter(published_date__range=[start_date, end_date]) \
                                        .annotate(rank=Window(
                                            expression=Rank(), 
                                            order_by=F('count_pages').desc())
                                        ).values('title', 'author', 'genre', 'count_pages', 'published_date', 'rank')
        except Exception as e:
            return Response({'message': f'{e}'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'books':books}, 
                        status=status.HTTP_200_OK)