from django.urls import path
from .views import book_list, homepage, OrderSummaryView, remove_from_cart, add_to_cart, search_item, filter_view
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
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)