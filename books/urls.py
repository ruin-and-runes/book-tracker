from django.urls import path
from . import views
from .views import reset_admin

urlpatterns = [
    path('', views.home, name='home'),
    path('stats/', views.stats, name='stats'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('reset-admin/', reset_admin),
]
