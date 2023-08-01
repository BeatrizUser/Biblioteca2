from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from biblioteca import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('livro/<str:bookId>/', views.livro_detalhado, name='livro_detalhado'),
    path('pesquisar/', views.buscar_livro, name='buscar_livro'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
