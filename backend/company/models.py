from django.db import models

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=200, unique=True)
    logo_path = models.CharField(max_length=200)
    description = models.TextField()
    website = models.URLField(blank=True, null=True)
    
    
    def __str__(self):
        return self.name