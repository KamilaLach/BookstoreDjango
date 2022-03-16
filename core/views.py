from django.shortcuts import render
from .models import Book
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


def homepage(request):
    return render(request, "home-page.html")

def book_list(request):
    context = {
        'books': Book.objects.all()
    }
    return render(request, "book_list.html", context)


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Welcome in Library!'}
        return Response(content)

