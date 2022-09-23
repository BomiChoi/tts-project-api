from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'project_id',
        'project_title',
        'updated_time',
        'created_time'
    )
