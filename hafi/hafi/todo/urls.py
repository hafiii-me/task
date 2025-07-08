# todo/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.dashboard, name='dashboard'), # This will be the home.html view
    path('task/create/', views.create_task, name='create_task'), # For adding tasks (Bonus)
    path('task/update/<int:pk>/', views.update_task, name='update_task'), # For updating tasks (Bonus)
    path('task/delete/<int:pk>/', views.delete_task, name='delete_task'), # For deleting tasks (Bonus)
]