from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'safe'

urlpatterns = [
    path('', views.password_list, name='list-password'),
    path('create/', views.create_password, name='create-password'),
    path('excluir/<int:id>', views.delete_password, name='delete-password'),

]