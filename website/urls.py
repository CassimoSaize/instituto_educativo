from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('curso/<int:curso_id>/', views.curso_detalhe, name='curso_detalhe'),
    path('matricula/', views.matricula_create, name='matricula_create'),
    path('matricula/sucesso/<int:matricula_id>/', views.matricula_sucesso, name='matricula_sucesso'),
]