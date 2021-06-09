from django.urls import path, include
from . import views

app_name = "myapp"

urlpatterns = [
    path('', views.index, name='index'),
    path('andamento', views.andamento, name='andamento'),
    path('colaborador', views.colaborador, name='colaborador'),
    path('pesquisarProjeto/<str:nome_projeto>', views.pesquisar_projeto, name="pesquisarProjeto"),
    path('detalheColaborador/<str:colaborador>', views.detalheColaborador, name="detalheColaborador"),
    path('negociacao', views.negociacao, name="negociacao"),
    path('match', views.match, name='match'),
]
