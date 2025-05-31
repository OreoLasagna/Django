from django.contrib import admin

# Register your models here.
from .models import Topic, Entry

#The . in front of models tells Django to look in the same directory as admin

admin.site.register(Topic)
admin.site.register(Entry)