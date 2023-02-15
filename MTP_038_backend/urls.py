from django.conf.urls import url
from django.urls import path, include
from MTP_038_backend import views

urlpatterns = [
    path('coordinates/', views.CoordinateView.as_view()),
]