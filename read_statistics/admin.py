from django.contrib import admin
from .models import ReadNum

@admin.register(ReadNum)
class RedNumAdmin(admin.ModelAdmin):
    list_display = ('read_num','content_object')
# Register your models here.
