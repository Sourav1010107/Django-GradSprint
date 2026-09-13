from django.urls import path
from . import views

app_name = "gradsprint"

urlpatterns = [
    path("test/", views.test_engine, name="test_engine"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("register/", views.register, name="register"),

    #==========================
    # API CALL: api\extensions
    #==========================

    path("test/<int:test_id>/", views.test_data, name="test_data"),
    path("save-answer/", views.save_answer, name="save_answer"),
    path("test/<int:test_id>/generate-result/", views.generate_test_result_view, name="generate_test_result"),
]


