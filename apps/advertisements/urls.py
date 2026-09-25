from django.urls import path
from apps.advertisements import views

urlpatterns = [
    path("", views.create_advertisement, name="create-advertisement"),
    path("<int:advertisement_id>", views.get_advertisement, name="get-advertisement"),
    path("user/<int:user_id>", views.list_for_user, name="list-advertisements-for-user"),
]
