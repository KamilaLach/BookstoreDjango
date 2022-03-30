from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import View

from .models import Book, Order, OrderBook
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class UserIDView(APIView):
    def get(self, request, *args, **kwargs):
        resp = {
            'is_admin': request.user.is_superuser,
            'email': request.user.email,
            'userID': request.user.id,
        }
        return render(request, "profile.html", resp)


def homepage(request):
    return render(request, "home-page.html")


def book_list(request):
    context = {
        'books': Book.objects.filter(available=True),
        'paginate_by': 1
    }
    return render(request, "book_list.html", context)


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, "order-summary.html", context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Welcome in Library!'}
        return Response(content)


def book_borrowed(request, slug):
    book = get_object_or_404(Book, slug=slug)
    order_book, created = OrderBook.objects.get_or_create(book=book,
                                                          user=request.user,
                                                          ordered=False)
    order_qs = Order.objects.filter(user=request.user,
                                    ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.books.filter(book__slug=book.slug).exists():
            book.available = False


@login_required
def add_to_cart(request, slug):
    book = get_object_or_404(Book, slug=slug)
    order_book, created = OrderBook.objects.get_or_create(book=book,
                                                          user=request.user,
                                                          ordered=False)
    order_qs = Order.objects.filter(user=request.user,
                                    ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # if the order item is in the order
        if order.books.filter(book__slug=book.slug).exists():
            book.available = False
            # order_book.quantity += 1
            order_book.save()
            messages.info(request, "You already have this book")
            return redirect("core:order-summary")
        else:
            order.books.add(order_book)
            # order.books.filter(book__slug=book.slug).update(available=False)
            book.available = False
            book.save()
            messages.info(request, "Book added to your cart!")
            return redirect("core:book-list")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.books.add(order_book)
        book.available = False
        book.save()
        messages.info(request, "Book added to your cart!")
    return redirect("core:book-list")


@login_required
def remove_from_cart(request, slug):
    book = get_object_or_404(Book, slug=slug)
    order_qs = Order.objects.filter(user=request.user,
                                    ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # if the order item is in the order
        if order.books.filter(book__slug=book.slug).exists():
            order_book = OrderBook.objects.filter(book=book,
                                                  user=request.user,
                                                  ordered=False)[0]
            order.books.remove(order_book)
            book.available = True
            book.save()
            messages.info(request, "Book removed from your cart!")
            return redirect("core:order-summary")
        else:
            messages.info(request, "Book is not placed in your cart!")
            return redirect("core:order-summary")
    else:
        # message that the user doesn't have the order
        messages.info(request, "You do not have an active order!")
        return redirect("core:order-summary")
    return redirect("core:order-summary")


def search_item(request):
    if request.method == "POST":
        searched = request.POST['searched']
        books = Book.objects.filter(title__contains=searched)
        context = {
            "searched": searched,
            "books": books
        }
        return render(request, "search_item.html", context)
    else:
        return render(request, "search_item.html")


def is_valid_queryparam(param):
    return param != '' and param is not None


def filter(request):
    qs = Book.objects.all()
    # categories = Category.objects.all()
    # producers = Producer.objects.all()
    title_contains_query = request.GET.get('title_contains')
    id_exact_query = request.GET.get('id_exact')
    # title_or_producer_query = request.GET.get('title_or_producer')
    author = request.GET.get('author')
    category = request.GET.get('category')

    if is_valid_queryparam(title_contains_query):
        qs = qs.filter(title__icontains=title_contains_query)

    # elif is_valid_queryparam(id_exact_query):
    #     qs = qs.filter(id=id_exact_query)

    # elif is_valid_queryparam(title_or_producer_query):
    #     qs = qs.filter(Q(title__icontains=title_or_producer_query) | Q(producer__name__icontains=title_or_producer_query)).distinct()

    if is_valid_queryparam(author):
        qs = qs.filter(price__lte=author)

    if is_valid_queryparam(category):
        qs = qs.filter(category__name=category)

    return qs


def filter_view(request):
    qs= filter(request)
    context = {
        'queryset': qs
    }
    return render(request, "book_list. html", context)
