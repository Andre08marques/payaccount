from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, CharField, TextField, Sum, Count
from django.db.models import F, Case, When, DecimalField
from django.db.models.functions import Coalesce
from django.utils import timezone
from decimal import Decimal
from .models import GrupoConta, ContaPagar, Faturamento  # ajuste o nome do modelo se necessário
from .forms import GrupoContaForm, ContaForm, FaturamentoForm
from datetime import timedelta


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


class ContaPagarListView(View):
    template_name = 'contas/conta_list.html'

    def get(self, request, *args, **kwargs):
        hoje = timezone.now().date()

        # -------------------------
        # QUERYSET BASE
        # -------------------------
        queryset = ContaPagar.objects.all()

        # -------------------------
        # FILTROS
        # -------------------------
        nome = request.GET.get('nome')
        grupo = request.GET.get('grupo')
        status = request.GET.get('status')
        recorrencia = request.GET.get('recorrencia')

        if nome:
            queryset = queryset.filter(nome_conta__icontains=nome)
        if grupo:
            queryset = queryset.filter(grupo_conta_id=grupo)
        if recorrencia:
            queryset = queryset.filter(recorrencia=recorrencia)
        
        # ← MUDANÇA: Aplicar filtro de status no queryset
        if status == 'em_dia':
            queryset = queryset.filter(data_vencimento__gt=hoje, pago=False)
        elif status == 'hoje':
            queryset = queryset.filter(data_vencimento=hoje, pago=False)
        elif status == 'atrasada':
            queryset = queryset.filter(data_vencimento__lt=hoje, pago=False)
        elif status == 'proximo_vencer':
            # Exemplo: contas que vencem nos próximos 7 dias
            proximo = hoje + timezone.timedelta(days=7)
            queryset = queryset.filter(
                data_vencimento__gt=hoje,
                data_vencimento__lte=proximo,
                pago=False
            )

        # -------------------------
        # PAGINAÇÃO
        # -------------------------
        paginator = Paginator(queryset.order_by('-id'), 100)
        page = request.GET.get('page')
        contas = paginator.get_page(page)

        # -------------------------
        # CÁLCULOS - BASEADO NO FILTRO (queryset filtrado)
        # -------------------------
        # ← MUDANÇA: Usar queryset filtrado ao invés de todas_contas
        contas_filtradas = queryset  # Usa o queryset já filtrado
        
        em_dia = contas_filtradas.filter(data_vencimento__gt=hoje, pago=False)
        vence_hoje = contas_filtradas.filter(data_vencimento=hoje, pago=False)
        atrasadas = contas_filtradas.filter(data_vencimento__lt=hoje, pago=False)
        
        # Opcional: também calcular próximo a vencer
        proximo = hoje + timezone.timedelta(days=7)
        proximo_vencer = contas_filtradas.filter(
            data_vencimento__gt=hoje,
            data_vencimento__lte=proximo,
            pago=False
        )

        # Total das contas filtradas
        total_contas = contas_filtradas.aggregate(total=Sum('valor'))['total'] or 0
        
        # Faturamento (mantém global)
        ultimo_faturamento = Faturamento.objects.order_by('-mes_referencia').first()
        valor_faturamento = ultimo_faturamento.valor if ultimo_faturamento else 0

        # -------------------------
        # CONTEXTO
        # -------------------------
        context = {
            'contas': contas,
            'hoje': hoje,

            # Totais baseados no filtro
            'total_contas': total_contas,
            'total_registros': contas_filtradas.count(),

            'total_em_dia': em_dia.aggregate(total=Sum('valor'))['total'] or 0,
            'qtd_em_dia': em_dia.count(),

            'total_vence_hoje': vence_hoje.aggregate(total=Sum('valor'))['total'] or 0,
            'qtd_vence_hoje': vence_hoje.count(),

            'total_atrasado': atrasadas.aggregate(total=Sum('valor'))['total'] or 0,
            'qtd_atrasadas': atrasadas.count(),
            
            # ← ADICIONE: Próximo a vencer
            'total_proximo_vencer': proximo_vencer.aggregate(total=Sum('valor'))['total'] or 0,
            'qtd_proximo_vencer': proximo_vencer.count(),

            # Faturamento (global)
            'faturamento': valor_faturamento,
            'lucro': valor_faturamento - total_contas,

            'grupos': GrupoConta.objects.all()
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        return self.get(request)




class ContaPagarCreateView(View):

    def get(self, request):
        form = ContaForm()
        context = {
            "form": form
        }
        return render(request, 'contas/conta_form.html', context)
    
    def post(self, request):
        form = ContaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro criado com sucesso!')
            return redirect('conta_list')
        
        # ← Quando houver erro, renderiza o template novamente com os erros
        messages.error(request, 'Não foi possível criar o registro. Verifique os campos.')
        return render(request, 'contas/conta_form.html', {'form': form})


class ContaPagarUpdateView(View):

    def get(self, request, pk):
        conta = get_object_or_404(ContaPagar, pk=pk)
        form = ContaForm(instance=conta)
        context = {
            "form": form,
            "object": conta
        }
        return render(request, 'contas/conta_edit.html', context)
    
    def post(self, request, pk):
        conta = get_object_or_404(ContaPagar, pk=pk)
        form = ContaForm(request.POST, request.FILES, instance=conta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro atualizado com sucesso!')
            return redirect('conta_list')
        
        messages.error(request, f"Não foi possível atualizar o registro. {form.errors}")
        return redirect('conta_list')

class ContaPagoView(View):

    def get(self, request, pk):
        conta = get_object_or_404(ContaPagar, pk=pk)
        conta.pago = True
        conta.data_pagamento = timezone.now().date()
        conta.status = 'em_dia'
        conta.save()
    
        messages.success(request, "Conta paga com sucesso!")
        return redirect('conta_list')


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
    form_class = FaturamentoForm
    template_name = 'faturamento/faturamento_form.html'
    success_url = reverse_lazy('faturamento_list')

    def form_valid(self, form):
        messages.success(self.request, 'Faturamento criado com sucesso!')
        return super().form_valid(form)


class FaturamentoUpdateView(View):
    def get(self, request, pk):
        faturamento = get_object_or_404(Faturamento, pk=pk)
        form = FaturamentoForm(instance=faturamento)
        
        # DEBUG
        print(f"DEBUG GET: Faturamento ID: {faturamento.pk}")
        print(f"DEBUG GET: PIX: {faturamento.FaturamentoModoBank_PIX}")
        print(f"DEBUG GET: Valor: {faturamento.valor}")
        
        context = {
            'form': form,
            'object': faturamento  # Importante!
        }
        return render(request, 'faturamento/faturamento_form.html', context)
    
    def post(self, request, pk):
        faturamento = get_object_or_404(Faturamento, pk=pk)
        form = FaturamentoForm(request.POST, instance=faturamento)
        print (form.errors)
        if form.is_valid():
            form.save()
            messages.success(request, 'Faturamento atualizado com sucesso!')
            return redirect('faturamento_list')
        
        context = {
            'form': form,
            'object': faturamento
        }
        return render(request, 'faturamento/faturamento_form.html', context)
class FaturamentoDeleteView(DeleteView):
    model = Faturamento
    template_name = 'faturamento/faturamento_confirm_delete.html'
    success_url = reverse_lazy('faturamento_list')

