from django.urls import path

from . import views
from .views import book_list, homepage, UserIDView, OrderSummaryView, remove_from_cart, add_to_cart, search_item, \
    filter_view, add_book, delete_book
from django.conf.urls.static import static
from django.conf import settings


app_name = 'core'

urlpatterns = [
    path('', homepage, name='homepage'),
    path('all-books', book_list, name='book-list'),
    path('summary', OrderSummaryView.as_view(), name='order-summary'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('all-books/search-item/', search_item, name='search-item'),
    path('all-books/filter-items/', filter_view, name='filter-items'),
    path('profile', UserIDView.as_view(), name='profile'),
    path('book/create/', add_book, name='book-create'),
    # path('book/update/', BookUpdateView.as_view(), name='book-update'),
    path('book/delete/<slug>/', delete_book, name='book-delete'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)