from django.urls import path
from . import views

urlpatterns = [
    path('logs/', views.LogList.as_view(), name="logs"),
    path('stat/', views.StatView.as_view(), name="stat"),
]