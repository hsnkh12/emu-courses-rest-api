from django.contrib import admin
from .models import Course, Resource, Department
# Register your models here.

admin.site.register(Course)
admin.site.register(Resource)
admin.site.register(Department)