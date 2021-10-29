from django.urls import path
from . import views

# URLConf i.e. URL configuration
urlpatterns = [
    path("home/", views.prototype_ui),
    path("form/", views.formgenerated_query)
]