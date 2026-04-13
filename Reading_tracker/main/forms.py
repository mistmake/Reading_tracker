from django import forms
from book.models import Book


class UploadBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['book_file']
        widgets = {
            'book_file': forms.FileInput(attrs={
                'style': 'font-family: Montserrat, serif',
                'id': 'epubFileInput',
                'accept': '.epub'
            })
        }
