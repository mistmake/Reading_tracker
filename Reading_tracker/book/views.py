import os
import zipfile

from django.shortcuts import render
from .forms import UploadBookForm
from .models import Book
from .file_readers.epub_reader_lector import EPUB
from Reading_tracker.settings import MEDIA_ROOT


BOOK_ROOT = os.path.join(MEDIA_ROOT, 'book_files')


def book(request):
    form = UploadBookForm(request.POST, request.FILES)
    if form.is_valid():
        uploaded_file = request.FILES['book_file']
        uploaded_name_only = uploaded_file.name
        if '.epub' == uploaded_file.name[-5:]:
            uploaded_name_only = uploaded_file.name[:-5]
        print(f'File uploaded: {uploaded_file}')
        dir_path = fr'book/books/{uploaded_name_only}/book_file/'
        print(f'Directory path: {dir_path}')
        os.makedirs(dir_path, exist_ok=True)
        print(f'Directory created')
        form.save()
        print('Form saved')
        book = Book.objects.get(book_file=fr'book_file/{uploaded_file.name}')
        print(f'Book: {book}')
        return render(request, 'book/book.html', context=create_compatible_epub(book, uploaded_file, dir_path))


def create_compatible_epub(book, uploaded_file, dir_path):
    with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
        style_file_name = r''

        for i in zip_ref.namelist():
            if '.css' in i:
                zip_ref.extract(i, dir_path)
                style_file_name = i
        print(f'Style file name: {style_file_name}')

        epub_processor = EPUB(os.path.join(BOOK_ROOT, uploaded_file.name), BOOK_ROOT)
        epub_processor.generate_content()
        epub_processor.generate_metadata()

        book.title = epub_processor.metadata[0]
        book.author = epub_processor.metadata[1]
        print(f'Book title: {book.title}')
        print(f'Book author: {book.author}')
        print('fuck u')
        book.save()

        prepared = []
        for chapter in epub_processor.content:
            prepared.append([chapter[0], chapter[1], chapter[2].replace('\n', '')])
        print('Content prepared')
        context = {'book_text': prepared, 'style': os.path.join('..', '..', dir_path, style_file_name)}
        print('Context created')
        return context
