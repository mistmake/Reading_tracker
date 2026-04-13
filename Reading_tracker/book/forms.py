from django import forms
from .models import Book


class UploadBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['book_file']