from django.urls import path
from library.views import *

urlpatterns = [
    path('get-book/', get_book, name="get_book"),
    path('add-book/', add_book, name="add_book"),
    path('update-book/', update_book, name="update_book"),
    path('delete-book/', delete_book, name="delete_book"),
]
