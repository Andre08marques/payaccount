from django import forms
from .models import GrupoConta, ContaPagar, Faturamento  # ajuste se o nome do model for diferente


class GrupoContaForm(forms.ModelForm):
    class Meta:
        model = GrupoConta
        fields = ['nome', 'descricao', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome do grupo'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Digite a descrição',
                'rows': 3
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class ContaForm(forms.ModelForm):
    FIELD_GROUPS = {
        'Informações Básicas': ['nome_conta', 'grupo_conta', 'fixo_variado', 'recorrencia'],
        'Dados Financeiros': ['valor', 'data_vencimento', 'pago', 'data_pagamento'],
        'Fornecedor': ['nome_razao', 'cpf_cnpj'],
        'Dados de Pagamento': ['tipo_pagamento', 'numero_conta_pix', 'agencia', 
                              'conta_corrente_poupanca', 'banco_origem'],
        'Veículo': ['modelo', 'placa', 'renavam', 'ano_fabricacao', 'ipva_multa'],
        'Dados de Acesso': ['link_acesso_pagamento', 'usuario', 'senha', 
                           'whatsapp_confirmacao', 'link_passo_passo', 'descricao_observacao']
    }

    class Meta:
        model = ContaPagar
        fields = '__all__'
        widgets = {
            'data_vencimento': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'data_pagamento': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Bootstrap nos widgets
        for name, field in self.fields.items():
            widget = field.widget
            if widget.__class__.__name__ not in ['DateInput']:  # Ignorar campos de data que já têm classe
                if widget.__class__.__name__ in ['CheckboxInput', 'CheckboxSelectMultiple', 'RadioSelect']:
                    widget.attrs['class'] = (widget.attrs.get('class', '') + ' form-check-input').strip()
                else:
                    widget.attrs['class'] = (widget.attrs.get('class', '') + ' form-control').strip()
            if not widget.attrs.get('placeholder') and getattr(field, 'label', None):
                widget.attrs['placeholder'] = field.label

        # Monta grupos para o template
        used = set()
        groups = []
        for group_label, field_names in (self.FIELD_GROUPS or {}).items():
            fields_in_group = [self[f] for f in field_names if f in self.fields]
            used.update([f for f in field_names if f in self.fields])
            if fields_in_group:
                groups.append((group_label, fields_in_group))

        remaining = [fname for fname in self.fields.keys() if fname not in used]
        if remaining:
            groups.append(('Outros', [self[f] for f in remaining]))

        self.grouped_fields = groups


class ContaPagarForm(forms.ModelForm):
    # Ajuste os grupos conforme os comentários do seu model:
    # Exemplo:
    # FIELD_GROUPS = {
    #     'Dados Básicos': ['titulo', 'descricao', 'ativo'],
    #     'Financeiro': ['valor', 'vencimento', 'pago'],
    #     'Vinculações': ['fornecedor', 'categoria', 'conta_bancaria'],
    # }
    FIELD_GROUPS = {
        # TODO: defina seus grupos e campos aqui
    }

    class Meta:
        model = ContaPagar
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Bootstrap nos widgets
        for name, field in self.fields.items():
            widget = field.widget
            wname = widget.__class__.__name__
            if wname in ['CheckboxInput', 'CheckboxSelectMultiple', 'RadioSelect']:
                widget.attrs['class'] = (widget.attrs.get('class', '') + ' form-check-input').strip()
            else:
                widget.attrs['class'] = (widget.attrs.get('class', '') + ' form-control').strip()
            if not widget.attrs.get('placeholder') and getattr(field, 'label', None):
                widget.attrs['placeholder'] = field.label

        # Monta grupos para os templates
        used = set()
        groups = []
        for group_label, field_names in (self.FIELD_GROUPS or {}).items():
            fields_in_group = [self[f] for f in field_names if f in self.fields]
            used.update([f for f in field_names if f in self.fields])
            if fields_in_group:
                groups.append((group_label, fields_in_group))

        remaining = [fname for fname in self.fields.keys() if fname not in used]
        if remaining:
            groups.append(('Outros', [self[f] for f in remaining]))

        self.grouped_fields = groups


class FaturamentoForm(forms.ModelForm):
    FIELD_GROUPS = {
        'Informações Básicas': ['descricao', 'tipo', 'valor', 'data'],
        'Detalhes': ['conta', 'observacao', 'comprovante'],
    }

    class Meta:
        model = Faturamento
        fields = '__all__'
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'conta': forms.Select(attrs={'class': 'form-select'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'comprovante': forms.FileInput(attrs={'class': 'form-control'}),
        }
