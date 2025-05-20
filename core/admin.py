from django.contrib import admin
from .models import CustomUser, Recipe, Comment, ContactMessage

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Recipe)
admin.site.register(Comment)
admin.site.register(ContactMessage)
