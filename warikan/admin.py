from django.contrib import admin
from warikan.models import Users, Categories, Expenses

# Register your models here.
admin.site.register([Users, Categories, Expenses])