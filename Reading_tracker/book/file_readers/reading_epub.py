import ebooklib
from ebooklib import epub
import epub_meta
import json


def get_text(file):
    book = epub.read_epub(file)
    data = book.metadata
    pretty = json.dumps(data, indent=4)
    # print(*data.values(), sep='\n')
    # for i in data.values():
    #     print(*i.values(), sep='\n')
    # metadata = epub_meta.get_epub_metadata(file, read_cover_image=True, read_toc=True)
    book_text = ''
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            book_text += item.get_body_content().decode('utf-8')
    return book_text



