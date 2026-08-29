from django.urls import path
from . import views

urlpatterns = [
    path("test/", views.test_engine, name="test_engine"),
    path("test/<int:test_id>/", views.test_data, name="test_data"),
]
