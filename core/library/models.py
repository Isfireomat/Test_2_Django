# from typing import List, Tuple
# from django.db import models

# class BaseModel(models.Model):
#     def save(self, *args, **kwargs) -> None:
#         self.full_clean()
#         super().save(*args, **kwargs)

#     class Meta:
#         abstract = True 

# class Table(BaseModel):
#     title = models.CharField(max_length=255, blank=False,  unique=True)
