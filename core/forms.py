from django import forms

from core.models import Book

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


class BookForm(forms.Form):
    title = forms.CharField(max_length=70)
    author = forms.CharField(max_length=70)
    category = forms.ChoiceField(choices=catchoice)
    description = forms.CharField(max_length=1000,
                                  widget=forms.Textarea(),
                                  help_text='Write here the description')
    slug = forms.SlugField()
    image = forms.ImageField()
    available = forms.BooleanField()

