from django.urls import path
from .views import book_list, homepage

app_name = 'core'

urlpatterns = [
    path('', homepage, name='homepage'),
    path('all-books/', book_list, name='book-list')
]