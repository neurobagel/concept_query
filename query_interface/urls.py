from django.urls import path

from . import views

# URLConf i.e. URL configuration
urlpatterns = [
    path("form/", views.formgenerated_query),
    path("download_csv/", views.download_csv)
]