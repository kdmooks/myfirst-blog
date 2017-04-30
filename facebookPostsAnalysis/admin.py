from django.contrib import admin
from .models import  Patient
from  .models import UserProfile

# Register your models here.
admin.site.register(Patient)
admin.site.register(UserProfile)