from django.contrib import admin

# Register your models here.
from .models import Patient, Disease
admin.site.register(Patient)
admin.site.register(Disease)