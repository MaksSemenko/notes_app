from django.contrib import admin
from .models import Note, Category


admin.site.register(Category)
admin.site.register(Note)
