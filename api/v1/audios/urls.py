from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProjectAudioListCreateView.as_view()),
    path('/<int:audio_id>', views.ProjectAudioDetailView.as_view()),
]
