from django.contrib import admin
from .models import *


class taskAdmin(admin.ModelAdmin):
    list_display  = ('title', 'completed', 'created_at')

admin.site.register(task, taskAdmin)
admin.site.register(users)
