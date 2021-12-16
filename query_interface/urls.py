from django.urls import path

from . import views

# URLConf i.e. URL configuration
urlpatterns = [
    path("", views.query_form),
    path("download_csv/", views.download_csv)
]