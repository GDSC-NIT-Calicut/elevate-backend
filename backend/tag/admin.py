from django.contrib import admin

# Register your models here.
from  .models import Tag, TagType
admin.site.register(Tag)
admin.site.register(TagType)