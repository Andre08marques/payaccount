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
                attrs={'class': 'form-control form-control-sm', 'type': 'date'}
            ),
            'data_pagamento': forms.DateInput(
                attrs={'class': 'form-control form-control-sm', 'type': 'date'}
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
                    widget.attrs['class'] = (widget.attrs.get('class', '') + ' form-control form-control-sm').strip()
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Força o valor da data no formato correto
        if self.instance and self.instance.pk and self.instance.mes_referencia:
            self.initial['mes_referencia'] = self.instance.mes_referencia.strftime('%Y-%m-%d')
    
    # Sobrescrever os campos para garantir formatação consistente
    FaturamentoModoBank_PIX = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        localize=False,  # Importante: desabilita formatação com vírgula
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0.01',
        })
    )
    
    FaturamentoLoja = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        localize=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0.01',
            
        })
    )

    FaturamentoModoBank_Cartao = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        localize=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0.01',
            'data-mask': 'real'
        })
    )
    
    FaturamentoEfiBank_Boleto = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        localize=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0.01',
            'data-mask': 'real'
        })
    )
    
    FaturamentoCelcoin_Cartao = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        localize=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0.01',
            'data-mask': 'real'
        })
    )
    
    FaturamentoMaquinaCartao = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        localize=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0.01',
            'data-mask': 'real'
        })
    )
    
    valor = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True,
        localize=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0.01',
            'readonly': 'readonly',
            
        })
    )
    
    mes_referencia = forms.DateField(
        localize=False,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date'
            },
            format='%Y-%m-%d'
        ),
        input_formats=['%Y-%m-%d', '%d/%m/%Y']
    )
    
    class Meta:
        model = Faturamento
        fields = [
            'mes_referencia',
            'FaturamentoModoBank_PIX',
            'FaturamentoModoBank_Cartao',
            'FaturamentoEfiBank_Boleto',
            'FaturamentoCelcoin_Cartao',
            'FaturamentoMaquinaCartao',
            'valor',
            'observacao'
        ]
        widgets = {
            'observacao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }
        labels = {
            'mes_referencia': 'Mês de Referência',
            'FaturamentoModoBank_PIX': 'Valor do Pagamento em Loja',
            'FaturamentoModoBank_Cartao': 'Valor do ModoBank Cartão',
            'FaturamentoEfiBank_Boleto': 'Valor do EfiBank Boleto',
            'FaturamentoCelcoin_Cartao': 'Valor do Faturamento Celcoin Cartão',
            'FaturamentoMaquinaCartao': 'Valor do Faturamento Maquina Cartão',
            'valor': 'Faturamento Bruto Total',
            'observacao': 'Observação',
        }