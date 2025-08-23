from django.db import models
from django.utils.html import mark_safe


# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    logo = models.ImageField(upload_to="company_logos/")
    description = models.TextField()
    
    def __str__(self):
        return self.name

    def logo_tag(self):
        if self.logo:
            return mark_safe(f'<img src="{self.logo.url}"width="50"/>')
        return ""
    logo_tag.short_description='logo'