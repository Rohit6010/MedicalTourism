from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Patient)
admin.site.register(Disease)
admin.site.register(Temp_info_1)
admin.site.register(Temp_info)