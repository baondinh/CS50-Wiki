from django.urls import path
from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("newentry", views.newentry, name="newentry"),
    path("randompage", views.randompage, name="randompage"),
    path("<str:title>", views.title, name="title"),
    path("search", views.search, name="search"), 
    path("edit/<str:title>", views.edit, name="edit")
]
