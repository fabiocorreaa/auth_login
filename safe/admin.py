from django.contrib import admin
from .models import SecretWord
# Register your models here.


class SecretWordAdmin(admin.ModelAdmin):
    list_display = ['id', 'url']


admin.site.register(SecretWord, SecretWordAdmin)
# Register your models here.
