from django.urls import path
from . import views

app_name = "gradsprint"

urlpatterns = [
    path("test/", views.test_engine, name="test_engine"),
    path("test/<int:test_id>/", views.test_data, name="test_data"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("register/", views.register, name="register"),
]
