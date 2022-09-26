from django.contrib import admin

from .models import Audio


# Register your models here.
@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'audio_id',
        'text',
        'speed',
        'project',
        'updated_time',
    )
