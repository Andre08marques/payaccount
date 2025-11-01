from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, CharField, TextField, Sum, Count
from django.db.models import F, Case, When, DecimalField
from django.db.models.functions import Coalesce
from django.utils import timezone
from decimal import Decimal
from .models import GrupoConta, ContaPagar, Faturamento  # ajuste o nome do modelo se necessário
from .forms import GrupoContaForm, ContaForm, FaturamentoForm

# Create your views here.

class GrupoContaListView(ListView):
    model = GrupoConta
    template_name = 'grupodecontas/grupoconta_list.html'
    context_object_name = 'grupos'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(nome__icontains=search)
        return queryset


class GrupoContaCreateView(CreateView):
    model = GrupoConta
    form_class = GrupoContaForm
    template_name = 'grupodecontas/grupoconta_form.html'
    success_url = reverse_lazy('grupoconta_list')

    def form_valid(self, form):
        messages.success(self.request, 'Grupo de conta criado com sucesso!')
        return super().form_valid(form)


class GrupoContaUpdateView(UpdateView):
    model = GrupoConta
    form_class = GrupoContaForm
    template_name = 'grupodecontas/grupoconta_form.html'
    success_url = reverse_lazy('grupoconta_list')

    def form_valid(self, form):
        messages.success(self.request, 'Grupo de conta atualizado com sucesso!')
        return super().form_valid(form)


class GrupoContaDeleteView(DeleteView):
    model = GrupoConta
    template_name = 'grupodecontas/grupoconta_confirm_delete.html'
    success_url = reverse_lazy('grupoconta_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Grupo de conta excluído com sucesso!')
        return super().delete(request, *args, **kwargs)


class ContaPagarListView(ListView):
    model = ContaPagar
    template_name = 'contas/conta_list.html'
    context_object_name = 'contas'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hoje = timezone.now().date()
        context['hoje'] = hoje  # Adicionando a data atual ao contexto
        
        # Busca todas as contas
        todas_contas = ContaPagar.objects.all()
        
        # Total das contas
        total_contas = todas_contas.aggregate(total=Sum('valor'))['total'] or 0
        context['total_contas'] = total_contas
        context['total_registros'] = todas_contas.count()
        
        # Contas em dia
        em_dia = todas_contas.filter(data_vencimento__gt=hoje, pago=False)
        context['total_em_dia'] = em_dia.aggregate(total=Sum('valor'))['total'] or 0
        context['qtd_em_dia'] = em_dia.count()
        
        # Contas que vencem hoje
        vence_hoje = todas_contas.filter(data_vencimento=hoje, pago=False)
        context['total_vence_hoje'] = vence_hoje.aggregate(total=Sum('valor'))['total'] or 0
        context['qtd_vence_hoje'] = vence_hoje.count()
        
        # Contas atrasadas
        atrasadas = todas_contas.filter(data_vencimento__lt=hoje, pago=False)
        context['total_atrasado'] = atrasadas.aggregate(total=Sum('valor'))['total'] or 0
        context['qtd_atrasadas'] = atrasadas.count()
        
        # Faturamento e Lucro
        ultimo_faturamento = Faturamento.objects.order_by('-mes_referencia').first()
        context['faturamento'] = ultimo_faturamento.valor if ultimo_faturamento else 0
        context['lucro'] = context['faturamento'] - total_contas if ultimo_faturamento else 0
        
        # Grupos para filtro
        context['grupos'] = GrupoConta.objects.all()
        
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtros do formulário
        nome = self.request.GET.get('nome')
        grupo = self.request.GET.get('grupo')
        status = self.request.GET.get('status')
        recorrencia = self.request.GET.get('recorrencia')
        tipo = self.request.GET.get('tipo')
        
        if nome:
            queryset = queryset.filter(nome_conta__icontains=nome)
        if grupo:
            queryset = queryset.filter(grupo_conta_id=grupo)
        if recorrencia:
            queryset = queryset.filter(recorrencia=recorrencia)
        if tipo:
            queryset = queryset.filter(fixo_variado=tipo)
            
        hoje = timezone.now().date()
        if status == 'em_dia':
            queryset = queryset.filter(data_vencimento__gt=hoje, pago=False)
        elif status == 'atrasada':
            queryset = queryset.filter(data_vencimento__lt=hoje, pago=False)
        elif status == 'hoje':
            queryset = queryset.filter(data_vencimento=hoje, pago=False)
            
        return queryset


class ContaPagarCreateView(CreateView):
    model = ContaPagar
    form_class = ContaForm
    template_name = 'contas/conta_form.html'
    success_url = reverse_lazy('conta_list')

    def form_valid(self, form):
        messages.success(self.request, 'Registro criado com sucesso!')
        return super().form_valid(form)


class ContaPagarUpdateView(UpdateView):
    model = ContaPagar
    form_class = ContaForm
    template_name = 'contas/conta_edit.html'
    success_url = reverse_lazy('conta_list')

    def form_valid(self, form):
        messages.success(self.request, 'Registro atualizado com sucesso!')
        return super().form_valid(form)


class ContaPagarDeleteView(DeleteView):
    model = ContaPagar
    template_name = 'contas/conta_confirm_delete.html'
    success_url = reverse_lazy('conta_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Registro excluído com sucesso!')
        return super().delete(request, *args, **kwargs)


class FaturamentoListView(ListView):
    model = Faturamento
    template_name = 'faturamento/faturamento_list.html'
    context_object_name = 'faturamentos'
    paginate_by = 10
    ordering = ['-mes_referencia']

class FaturamentoCreateView(CreateView):
    model = Faturamento
    template_name = 'faturamento/faturamento_form.html'
    fields = ['mes_referencia', 'valor', 'observacao']
    success_url = reverse_lazy('faturamento_list')

    def form_valid(self, form):
        messages.success(self.request, 'Faturamento registrado com sucesso!')
        return super().form_valid(form)

class FaturamentoUpdateView(UpdateView):
    model = Faturamento
    template_name = 'faturamento/faturamento_form.html'
    fields = ['mes_referencia', 'valor', 'observacao']
    success_url = reverse_lazy('faturamento_list')

    def form_valid(self, form):
        messages.success(self.request, 'Faturamento atualizado com sucesso!')
        return super().form_valid(form)

class FaturamentoDeleteView(DeleteView):
    model = Faturamento
    template_name = 'faturamento/faturamento_confirm_delete.html'
    success_url = reverse_lazy('faturamento_list')
