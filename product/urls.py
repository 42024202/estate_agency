from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("work-single/", views.work_single, name="work-single"),
    path("all_announcenments/", views.all_announcenments, name="all_announcenments"),
]
