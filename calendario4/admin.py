from django.contrib import admin

from .models import Category, Color, MyUser, Team

# Register your models here.
admin.site.register(MyUser)
admin.site.register(Team)
admin.site.register(Category)
admin.site.register(Color)
