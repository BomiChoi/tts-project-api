from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProjectAudioListCreateView.as_view()),
]
