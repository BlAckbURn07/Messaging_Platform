from django.contrib import admin

from .models import Room, Genre, Message

admin.site.register(Room)
admin.site.register(Genre)
admin.site.register(Message)

# Register your models here.
