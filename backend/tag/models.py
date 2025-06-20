from django.db import models

# Create your models here.

class TagType(models.Model):
    name= models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name
        
class Tag(models.Model):
    title = models.CharField(max_length=100, unique=True)
    type= models.ForeignKey(TagType,on_delete=models.SET_NULL,null=True,blank=True)
    def __str__(self):
        return f"{self.title}- {self.type.name if self.type else 'No Type'}" 