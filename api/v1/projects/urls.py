from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.ProjectCreateView.as_view()),
    path('/<int:pk>', views.ProjectDestroyView.as_view()),
    path('/<int:pk>/audios', include('api.v1.audios.urls')),
]
