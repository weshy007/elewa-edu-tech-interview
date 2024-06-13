from django.contrib import admin

from .models import CustomUser, Department, Task

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Department)
admin.site.register(Task)