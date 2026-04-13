from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=100, null=True, default='Untitled')
    author = models.CharField(max_length=100, null=True, default='Unknown')
    book_file = models.FileField(upload_to='book_files/', null=True)
    style = models.FilePathField(default=r'/book/static/book/book_styles/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
