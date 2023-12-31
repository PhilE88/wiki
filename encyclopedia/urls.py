from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:article>", views.article, name="article"),
    path("search/", views.search, name="search"),
    path("newEntry/", views.newEntry, name="newEntry"),
    path("edit/<str:entry>", views.edit, name="edit")
]
