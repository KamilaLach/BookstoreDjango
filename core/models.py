from django.db import models
from django.conf import settings
from django.shortcuts import reverse


class Book(models.Model):
    catchoice = [
        ('Education', 'Education'),
        ('Comics', 'Comics'),
        ('Biography', 'Biography'),
        ('History', 'History'),
        ('Novel', 'Novel'),
        ('Fantasy', 'Fantasy'),
        ('Thriller', 'Thriller'),
        ('Romance', 'Romance'),
        ('Sci-Fi', 'Sci-Fi')
    ]
    title = models.CharField(max_length=70,
                             blank=False,
                             default='')
    author = models.CharField(max_length=70,
                              blank=False,
                              default='')
    category = models.CharField(max_length=30,
                                choices=catchoice,
                                default='Education')
    description = models.CharField(max_length=1000,
                                   default='')
    slug = models.SlugField()
    image = models.ImageField()
    available = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })

    class Meta:
        ordering = ['title']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'


class OrderBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.book.title


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    books = models.ManyToManyField(OrderBook)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
