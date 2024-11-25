from typing import List, Tuple
from django.db import models

class BaseModel(models.Model):
    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True 

class Book(BaseModel):
    title = models.CharField(max_length=255, blank=False,  unique=True)
    author = models.CharField(max_length=255, blank=False)
    genre = models.CharField(max_length=255)
    count_pages = models.IntegerField(blank=False)
    epub = models.BinaryField(null=True)
    published_date = models.DateField(blank=False)
    create_date_time = models.DateTimeField(auto_now_add=True)