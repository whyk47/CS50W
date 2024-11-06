from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.page, name="page"),
    path("search/<str:query>", views.search, name="search"),
    path("new_page/", views.new_page, name="new_page"),
    path("edit/<str:name>", views.edit_page, name="edit_page"),
    path("random/", views.rand_page, name="random")
]