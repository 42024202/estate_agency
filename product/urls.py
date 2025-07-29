from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("work-single/", views.work_single, name="work-single"),
    path("all_announcenments/", views.all_announcenments, name="all_announcenments"),

    # Autentification
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),

]
