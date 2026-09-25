from django.urls import path
from apps.detection import views

urlpatterns = [
    path("analyse-credibility", views.analyse_credibility, name="analyse-credibility"),
    path("predict", views.predict, name="predict"),
    path("predictions/<int:prediction_id>", views.get_prediction, name="get-prediction"),
    path("explanations/<int:prediction_id>", views.get_explanation, name="get-explanation"),
    path("health", views.health, name="health"),
]
