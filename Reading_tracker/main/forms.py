from django import forms
from django.core.exceptions import ValidationError
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

    def clean_book_file(self):
        file = self.cleaned_data.get('book_file')
        if file and not file.name.endswith('.epub'):
            raise ValidationError('Only .epub files are supported')
        return file
