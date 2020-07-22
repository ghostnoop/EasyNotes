from django.contrib import admin

# Register your models here.
from .models import User,NoteBoard

admin.site.register(User)
admin.site.register(NoteBoard)