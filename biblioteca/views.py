from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.urls import reverse
import requests
from .models import Livro

# Create your views here.
def buscar_livro(request):
    search_query = request.GET.get('q', '')
    if search_query:
        url = f'https://www.googleapis.com/books/v1/volumes?q={search_query}'
        response = requests.get(url)
        data = response.json()

        books = []
        if 'items' in data:
            for item in data['items']:
                titulo = item['volumeInfo'].get('title', 'Desconhecido')
                autor = ', '.join(item['volumeInfo'].get('authors', ['Desconhecido']))
                editora = item['volumeInfo'].get('publisher', 'Editora desconhecida.')
                ano_public = item['volumeInfo'].get('publishedDate', '')
                cover_url = item['volumeInfo']['imageLinks']['thumbnail'] if 'imageLinks' in item['volumeInfo'] and 'thumbnail' in item['volumeInfo']['imageLinks'] else None
                
                book = {
                    'title': titulo,
                    'author': autor,
                    'publisher': editora,
                    'publishedDate': ano_public,
                    'cover_url' : cover_url
                }
                books.append(book)
    else:
        books = []
        search_query = ''

    return render(request, 'buscar_livro.html', {'books': books, 'search_query': search_query})
