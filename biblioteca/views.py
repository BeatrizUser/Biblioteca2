from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.urls import reverse
import requests
from .models import Livro

# Create your views here.
def buscar_livro(request):
    bookId = request.GET.get('q', '')
    if bookId:
        url = f'https://www.googleapis.com/books/v1/volumes?q={bookId}'
        response = requests.get(url)
        data = response.json()

        books = []
        if 'items' in data:
            for item in data['items']:
                bookId = item['id']
                titulo = item['volumeInfo'].get('title', 'Desconhecido')
                autor = ', '.join(item['volumeInfo'].get('authors', ['Desconhecido']))
                editora = item['volumeInfo'].get('publisher', 'Editora desconhecida.')
                ano_public = item['volumeInfo'].get('publishedDate', '')
                cover_url = item['volumeInfo']['imageLinks']['thumbnail'] if 'imageLinks' in item['volumeInfo'] and 'thumbnail' in item['volumeInfo']['imageLinks'] else None
                
                book = {
                    'id': bookId,
                    'title': titulo,
                    'author': autor,
                    'publisher': editora,
                    'publishedDate': ano_public,
                    'cover_url' : cover_url
                }
                books.append(book)
    else:
        books = []
        bookId = ''

    return render(request, 'buscar_livro.html', {'books': books, 'bookId': bookId})

def livro_detalhado(request, bookId):
    if bookId:
        url = f'https://www.googleapis.com/books/v1/volumes/{bookId}'
        response = requests.get(url)
        data = response.json()

        livro = None
        if 'volumeInfo' in data:
            book_Id = data['id']
            volume_info = data['volumeInfo']
            titulo = volume_info.get('title', 'Desconhecido')
            autor = ', '.join(volume_info.get('authors', ['Desconhecido']))
            editora = volume_info.get('publisher', 'Editora desconhecida.')
            ano_public = volume_info.get('publishedDate', '')
            descricao = volume_info.get('description', 'Não Possui descrição.')
            cover_url = volume_info['imageLinks']['thumbnail']
            previewLink = volume_info.get('previewLink', 'Desconhecido')

            livro = {
                'id': book_Id,
                'title': titulo,
                'author': autor,
                'publisher': editora,
                'publishedDate': ano_public,
                'descricao': descricao,
                'cover_url': cover_url,
                'previewLink': previewLink
            }

    return render(request, 'livro_detalhado.html', {'livro': livro})