from django.urls import path

from . import views

app_name = 'inventory'
urlpatterns = [
    path('', views.index, name='index'),
    path('modify/<int:id>/', views.modify, name='modify'),
    path('results/', views.results, name='results'),
    path('asset/<int:id>/', views.asset, name='asset'),
    path('user/<int:id>/', views.user, name='user'),
]