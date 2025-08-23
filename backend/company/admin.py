from django.contrib import admin

# Register your models here.
from .models import Company


class CompanyAdmin(admin.ModelAdmin):
    list_display=['name','logo_tag']

admin.site.register(Company,CompanyAdmin)