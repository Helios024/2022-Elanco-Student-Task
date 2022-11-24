from django.contrib import admin

# Register your models here.
from .models import ElancoData , Resources

admin.site.register(ElancoData)
admin.site.register(Resources)