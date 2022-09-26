from django.contrib import admin

from apps.audio.models import Audio
from .models import Project


class AudioInline(admin.TabularInline):
    model = Audio


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'project_id',
        'project_title',
        'updated_time',
        'created_time',
    )
    inlines = (AudioInline,)
