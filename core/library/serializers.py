from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'count_pages', 'epub', 'published_date']

    def create(self, validated_data):
        epub = validated_data.get('epub')
        if epub:
            validated_data['epub'] = epub.read()
        return super().create(validated_data)

class BookListSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()