# todoproject/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), # For login, logout, password reset
    path('', RedirectView.as_view(url='dashboard/', permanent=False)), # Redirect root to dashboard
    path('dashboard/', include('todo.urls')), # Include todo app URLs
]