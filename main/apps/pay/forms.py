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
                attrs={'class': 'form-control form-control-sm', 'type': 'date'},
                format='%Y-%m-%d'  # ← ADICIONE ESTA LINHA
            ),
            'data_pagamento': forms.DateInput(
                attrs={'class': 'form-control form-control-sm', 'type': 'date'},
                format='%Y-%m-%d'  # ← ADICIONE ESTA LINHA
            ),
            'valor': forms.TextInput(  # ← ADICIONE ISSO
                attrs={
                    'class': 'form-control form-control-sm money-input',
                    'placeholder': 'R$ 0,00'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # ← ADICIONE ESTAS LINHAS AQUI (antes do loop do Bootstrap)
        if self.instance and self.instance.pk:
            if self.instance.data_vencimento:
                self.initial['data_vencimento'] = self.instance.data_vencimento.strftime('%Y-%m-%d')
            if self.instance.data_pagamento:
                self.initial['data_pagamento'] = self.instance.data_pagamento.strftime('%Y-%m-%d')
        
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
    
    def clean_FaturamentoLoja(self):
        valor = self.cleaned_data.get('FaturamentoLoja')
        return self._limpar_valor_monetario(valor)
    
    def clean_FaturamentoModoBank_PIX(self):
        valor = self.cleaned_data.get('FaturamentoModoBank_PIX')
        return self._limpar_valor_monetario(valor)
    
    def clean_FaturamentoModoBank_Cartao(self):
        valor = self.cleaned_data.get('FaturamentoModoBank_Cartao')
        return self._limpar_valor_monetario(valor)
    
    def clean_FaturamentoEfiBank_Boleto(self):
        valor = self.cleaned_data.get('FaturamentoEfiBank_Boleto')
        return self._limpar_valor_monetario(valor)
    
    def clean_FaturamentoCelcoin_Cartao(self):
        valor = self.cleaned_data.get('FaturamentoCelcoin_Cartao')
        return self._limpar_valor_monetario(valor)
    
    def clean_FaturamentoMaquinaCartao(self):
        valor = self.cleaned_data.get('FaturamentoMaquinaCartao')
        return self._limpar_valor_monetario(valor)
    
    def clean_valor(self):
        valor = self.cleaned_data.get('valor')
        return self._limpar_valor_monetario(valor)
    
    def _limpar_valor_monetario(self, valor):
        """
        Converte valores monetários formatados (ex: "1.234,56" ou "1234.56") 
        para Decimal válido
        """
        from decimal import Decimal, InvalidOperation
        
        if valor is None or valor == '':
            return Decimal('0.00')
        
        # Se já for Decimal, retorna
        if isinstance(valor, Decimal):
            return valor
        
        # Converte para string e limpa
        valor_str = str(valor).strip()
        
        # Remove espaços e símbolo de moeda
        valor_str = valor_str.replace('R$', '').replace(' ', '')
        
        # Verifica se tem vírgula (formato brasileiro)
        if ',' in valor_str:
            # Remove pontos (separadores de milhar) e troca vírgula por ponto
            valor_str = valor_str.replace('.', '').replace(',', '.')
        
        try:
            return Decimal(valor_str)
        except (InvalidOperation, ValueError):
            raise forms.ValidationError('Informe um valor monetário válido.')
    
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
            'FaturamentoLoja',
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
            'FaturamentoLoja': forms.TextInput(attrs={
                'class': 'form-control money-input',
                'placeholder': '0,00',
                'type': 'text'
            }),
            'FaturamentoModoBank_PIX': forms.TextInput(attrs={
                'class': 'form-control money-input',
                'placeholder': '0,00'
            }),
            'FaturamentoModoBank_Cartao': forms.TextInput(attrs={
                'class': 'form-control money-input',
                'placeholder': '0,00'
            }),
            'FaturamentoEfiBank_Boleto': forms.TextInput(attrs={
                'class': 'form-control money-input',
                'placeholder': '0,00'
            }),
            'FaturamentoCelcoin_Cartao': forms.TextInput(attrs={
                'class': 'form-control money-input',
                'placeholder': '0,00'
            }),
            'FaturamentoMaquinaCartao': forms.TextInput(attrs={
                'class': 'form-control money-input',
                'placeholder': '0,00'
            }),
            'valor': forms.TextInput(attrs={
                'class': 'form-control money-input',
                'placeholder': '0,00',
                'readonly': 'readonly'
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