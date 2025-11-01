from django.urls import path
from .views import (
    GrupoContaListView,
    GrupoContaCreateView,
    GrupoContaUpdateView,
    GrupoContaDeleteView,
    ContaPagarListView, 
    ContaPagarCreateView, 
    ContaPagarUpdateView, 
    ContaPagarDeleteView,
    FaturamentoListView, 
    FaturamentoCreateView, 
    FaturamentoUpdateView, 
    FaturamentoDeleteView
)

urlpatterns = [
    path('grupos-conta/', GrupoContaListView.as_view(), name='grupoconta_list'),
    path('grupos-conta/novo/', GrupoContaCreateView.as_view(), name='grupoconta_create'),
    path('grupos-conta/<int:pk>/editar/', GrupoContaUpdateView.as_view(), name='grupoconta_update'),
    path('grupos-conta/<int:pk>/excluir/', GrupoContaDeleteView.as_view(), name='grupoconta_delete'),
    path('contas/',                       ContaPagarListView.as_view(),   name='conta_list'),
    path('contas/novo/',                  ContaPagarCreateView.as_view(), name='conta_create'),
    path('contas/<int:pk>/editar/',       ContaPagarUpdateView.as_view(), name='conta_update'),
    path('contas/<int:pk>/excluir/',      ContaPagarDeleteView.as_view(), name='conta_delete'),
    path('faturamento/',                 FaturamentoListView.as_view(), name='faturamento_list'),
    path('faturamento/novo/',            FaturamentoCreateView.as_view(), name='faturamento_create'),
    path('faturamento/<int:pk>/editar/', FaturamentoUpdateView.as_view(), name='faturamento_update'),
    path('faturamento/<int:pk>/excluir/', FaturamentoDeleteView.as_view(), name='faturamento_delete'),
]