from django.db import models

# Create your models here.
class Tag(models.Model):
    title = models.CharField(max_length=100, unique=True)
    type= models.CharField(max_length=100,blank=True, null=True)
    def __str__(self):
        return self.title