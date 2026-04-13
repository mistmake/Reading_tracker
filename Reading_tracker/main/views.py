import os.path
import os
import zipfile

from django.shortcuts import render, redirect
from bs4 import BeautifulSoup
from .forms import UploadBookForm
from book.file_readers.epub_reader_lector import EPUB
from Reading_tracker.settings import MEDIA_ROOT
from book.models import Book
from django.db import models
from user.models import ReadingList
from django.template.loader import render_to_string
from django.template import Template, Context


BOOK_ROOT = os.path.join(MEDIA_ROOT, 'book_files')


def index(request):
    if request.method == 'POST':
        form = UploadBookForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['book_file']
            uploaded_name_only = uploaded_file.name
            if '.epub' == uploaded_file.name[-5:]:
                uploaded_name_only = uploaded_file.name[:-5]
            print(f'File uploaded: {uploaded_file}')

            dir_path = os.path.join('book', 'books', 'static', uploaded_name_only)
            print(f'Directory path: {dir_path}')

            os.makedirs(dir_path, exist_ok=True)
            print(f'Directory created ')

            form.save()
            print('Form saved')

            book = form.instance
            reader_id = request.user
            book.style = dir_path
            print(f'Book: {book}')

            return render(request,
                          'book/book.html',
                          context=create_compatible_epub(book,
                                                         uploaded_file,
                                                         dir_path,
                                                         reader_id,
                                                         uploaded_name_only=uploaded_name_only))
    else:
        form = UploadBookForm()
    return render(request, 'main/index.html', {'form': form})


def create_compatible_epub(book, uploaded_file, dir_path, reader_id, uploaded_name_only='', ):
    with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
        css_files_list = []

        font_extensions = ['.ttf', '.otf', '.woff']
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.svg']

        for file in zip_ref.namelist():
            if '.css' in file:
                zip_ref.extract(file, dir_path)
                css_files_list.append(file)
            elif file.endswith(tuple(font_extensions)):
                zip_ref.extract(file, dir_path)
            elif file.endswith(tuple(image_extensions)):
                zip_ref.extract(file, dir_path)

        print(f'Style filenames: {css_files_list}')

        epub_processor = EPUB(os.path.join(BOOK_ROOT, uploaded_file.name), BOOK_ROOT)
        epub_processor.generate_content()
        epub_processor.generate_metadata()

        book.title = epub_processor.metadata[0]
        book.author = epub_processor.metadata[1]
        book.style = dir_path

        rlist = ReadingList.objects.create(reader_id=reader_id, book_id=book)
        rlist.save()

        print(f'Book title: {book.title}')
        print(f'Book author: {book.author}')
        book.save()

        prepared = []
        for chapter in epub_processor.content:
            chapter = list(chapter)
            chapter[2] = chapter[2].replace('\n', '')
            chapter[2] = chapter[2] = chapter[2].replace('<title>', '')  # fixme: find better solution
            chapter[2] = chapter[2] = chapter[2].replace('<title/>', '')
            chapter[2] = replace_links(chapter[2], uploaded_name_only)
            # chapter[2] = replace_sources(chapter[2])
            prepared.append([chapter[0], chapter[1], chapter[2]])
        print('Content prepared')
        context = {'book_text': prepared,
                   'styles': [os.path.join(uploaded_name_only, i) for i in css_files_list],
                   'title': epub_processor.metadata[0],
                   'author': epub_processor.metadata[1],
                   'chapter_num': len(prepared)}
        print('Context created')
        print(f'Style path: {context["styles"]}')
        return context


def replace_links(chapter: str, uploaded_name_only):
    soup = BeautifulSoup(chapter, 'html.parser')
    for link in soup.find_all('a'):
        if 'href' in link.attrs:
            link['href'] = "{% static '" + uploaded_name_only + link['href'] + "' %}"
    for element in soup.find_all(src=True):
        element['src'] = "{% static '" + uploaded_name_only + "/OPF/" + element['src'] + "' %}"
    chapter = str(soup)
    chapter = '{% load static %}' + chapter
    template = Template(chapter)
    rendered = template.render(Context())
    return rendered

