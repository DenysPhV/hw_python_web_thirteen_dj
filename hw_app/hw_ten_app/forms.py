from django.forms import ModelForm, CharField, TextInput, DateField, SelectDateWidget

from .models import Author, Tag, Quote


class AuthorForm(ModelForm):
    fullname = CharField(max_length=150, required=True, widget=TextInput())
    born_date = DateField(widget=SelectDateWidget(years=[i for i in range(1800, 2023)]))
    born_location = CharField(max_length=150, widget=TextInput())
    description = CharField(max_length=1000, widget=TextInput())

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']


class TagForm(ModelForm):
    name = CharField(min_length=3, max_length=25, required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ['name']


class QuoteForm(ModelForm):
    author = CharField(min_length=1, max_length=150, widget=TextInput())
    quote = CharField(min_length=5, max_length=500, required=True, widget=TextInput())

    class Meta:
        model = Quote
        fields = ['quote']
        exclude = ['tags', 'author']
