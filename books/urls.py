from django.urls import path
from . import views
from .views import load_books
from .views import load_tropes

urlpatterns = [
    path('', views.home, name='home'),
    path('stats/', views.stats, name='stats'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('load-books/', load_books),
    path('load-tropes/', load_tropes),
    path('create-admin/', views.create_admin),
 ]
