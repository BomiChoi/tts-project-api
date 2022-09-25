from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProjectCreateView.as_view()),
    path('/<int:pk>', views.ProjectDestroyView.as_view())
]
