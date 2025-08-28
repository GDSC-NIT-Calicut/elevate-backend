from django.db import models

from user.models import User
from company.models import Company
from tag.models import Tag

# Create your models here.

class Experience(models.Model):
    cover_image= models.ImageField(upload_to='experience_images/',null=True,blank=True)

    title = models.CharField(max_length=200)
    role = models.CharField(max_length=100)
    
    short_description = models.TextField()
    content = models.JSONField(null=True, blank=True)
    tips=models.TextField(null=True, blank=True)
    
    published_date = models.DateTimeField(auto_now_add=True)
    experience_date = models.DateField()
    visibility=models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
    compensation=models.TextField(null=True, blank=True)
    job_type=models.CharField(max_length=20, choices=[
        ('fte', 'fte'),
        ('internship', 'internship'),
        ('research','research'),
        ('other', 'other')
    ])
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='experiences')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='experiences')
    tags=models.ManyToManyField(Tag, related_name='experiences', blank=True)

    saved_by=models.ManyToManyField(User, related_name='saved_experiences', blank=True)
    def __str__(self):
        return f" {self.author.name} | {self.company.name} | {self.title}"