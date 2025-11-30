from django.db import models


from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class GrupoConta(models.Model):
    """Grupo de categorização das contas"""
    nome = models.CharField(max_length=100, verbose_name='Nome')
    descricao = models.TextField(blank=True, null=True, verbose_name='Descrição')
    ativo = models.BooleanField(default=True, null=True, verbose_name='Ativo')
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True,null=True, verbose_name='Atualizado em')

    class Meta:
        verbose_name = 'Grupo de Conta'
        verbose_name_plural = 'Grupos de Contas'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class ContaPagar(models.Model):
    """Model principal para contas a pagar"""
    
    TIPO_CONTA_CHOICES = [
        ('fixo', 'Fixo'),
        ('variado', 'Variado'),
    ]
    
    TIPO_PAGAMENTO_CHOICES = [
        ('transferencia', 'Transferência'),
        ('deposito', 'Depósito'),
        ('pix_cpf', 'Pix CPF'),
        ('pix_cnpj', 'Pix CNPJ'),
        ('pix_email', 'Pix E-mail'),
        ('pix_telefone', 'Pix Telefone'),
        ('pix_chave_aleatoria', 'Pix Chave Aleatória'),
        ('especie', 'Espécie (Dinheiro)'),
        ('boleto', 'Boleto Bancário'),
        ('cartao_credito', 'Cartão de Crédito'),
        ('cartao_debito', 'Cartão de Débito'),
        ('debito_automatico', 'Débito Automático'),
        ('link_pagamento', 'Link de Pagamento'),
        ('pix_qr_code', 'Pix QR Code'),
    ]
    
    RECORRENCIA_CHOICES = [
        ('unica', 'Única'),
        ('mensal', 'Mensal'),
        ('bimestral', 'Bimestral'),
        ('trimestral', 'Trimestral'),
        ('semestral', 'Semestral'),
        ('anual', 'Anual'),
    ]

    ipva_multa_choices = [
        ('ipva', 'IPVA'),
        ('multa', 'Multa'),
        ('ipva+multa', 'IPVA + Multa'),
    ]
    
    BANK_CHOICES = [
    ("caixa", "Caixa Econômica Federal"),
    ("bb", "Banco do Brasil"),
    ("itau", "Itaú Unibanco"),
    ("bradesco", "Bradesco"),
    ("santander", "Santander Brasil"),
    ("nubank", "Nubank"),
    ("inter", "Banco Inter"),
    ("c6", "C6 Bank"),
    ("original", "Banco Original"),
    ("pan", "Banco Pan"),
    ("safra", "Banco Safra"),
    ("mercantil", "Banco Mercantil do Brasil"),
    ("banrisul", "Banrisul (Banco do Estado do Rio Grande do Sul)"),
    ("bv", "Banco Votorantim (BV)"),
    ("daycoval", "Banco Daycoval"),
    ("bs2", "Banco BS2"),
    ("digio", "Banco Digio"),
    ("sicredi", "Banco Cooperativo Sicredi"),
    ("sicoob", "Banco Cooperativo Sicoob"),
    ("bnb", "Banco do Nordeste do Brasil"),
    ("banestes", "Banestes (Banco do Estado do Espírito Santo)"),
    ("alfa", "Banco Alfa"),
    ("modal", "Banco Modal"),
    ("pine", "Banco Pine"),
    ("rendimento", "Banco Rendimento"),
    ("rodobens", "Banco Rodobens"),
    ("amazonia", "Banco da Amazônia"),
    ("kebhana", "Banco KEB Hana do Brasil"),
    ("johndeere", "Banco John Deere"),
    ("mizuho", "Banco Mizuho do Brasil"),
    ("outros", "Outros não cadastrados"),
   ]
    
    STATUS_CHOICES = [
        ('em_dia', '🟢 Em Dia'),
        ('prox_vencer', '🟡 Próximo a Vencer'),
        ('vence_hoje', '🟠 Vence Hoje'),
        ('atrasado', '🔴 Em Atraso'),
        
    ]
    
    
    ACCOUNT_TYPE_CHOICES = [
    ("corrente", "Conta Corrente"),
    ("poupanca", "Conta Poupança"),
    ("pix", "Pix"),
    ]
    # Informações básicas
    nome_conta = models.CharField(
        max_length=200,
        verbose_name="Nome da Conta",
        help_text="Nome identificador da conta"
    )
    
    grupo_conta = models.ForeignKey(
        GrupoConta,
        on_delete=models.PROTECT,
        related_name='contas',
        verbose_name="Grupo de Conta"
    )

    alertar_dias_antes = models.PositiveIntegerField(
        verbose_name="Alertar quantos dias antes",
        default=0,
        help_text="Número de dias antes do vencimento para enviar o alerta."
    )
    
    fixo_variado = models.CharField(
        max_length=10,
        choices=TIPO_CONTA_CHOICES,
        verbose_name="Valor Fixo ou Variado"
    )
    
    recorrencia = models.CharField(
        max_length=20,
        choices=RECORRENCIA_CHOICES,

        verbose_name="Recorrência"
    )
    
    # Dados financeiros
    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Valor"
    )
    
    data_vencimento = models.DateField(
        verbose_name="Data de Vencimento"
    )
    
    # Informações do fornecedor/destinatário
    nome_razao = models.CharField(
        max_length=200,
        verbose_name="Nome/Razão Social",
        blank=True
    )
    
    cpf_cnpj = models.CharField(
        max_length=18,
        verbose_name="CPF/CNPJ",
        blank=True,
        help_text="Formato: 000.000.000-00 ou 00.000.000/0000-00"
    )
    
    # Dados de pagamento
    tipo_pagamento = models.CharField(
        max_length=20,
        choices=TIPO_PAGAMENTO_CHOICES,
        verbose_name="Transferência/Depósito/Pix",
        blank=True
    )
    
    nome_pix = models.CharField(
        max_length=300,
        verbose_name="Nome da Conta ou Pix",
        blank=True
    )

    numero_conta_pix = models.CharField(
        max_length=300,
        verbose_name="Número da Conta ou Pix",
        blank=True
    )
    
    agencia = models.CharField(
        max_length=10,
        verbose_name="Agência",
        blank=True
    )
    
    conta_corrente_poupanca = models.CharField(
        max_length=50,
        choices=ACCOUNT_TYPE_CHOICES,
        verbose_name="Conta Corrente ou Poupança",
        blank=True
    )
    
    banco_origem = models.CharField(
        max_length=100,
        choices=BANK_CHOICES,
        verbose_name="Banco de Origem",
        blank=True
    )
    
    # Informações complementares de veículo
    modelo = models.CharField(
        max_length=100,
        verbose_name="Modelo",
        blank=True,
        help_text="Modelo do veículo (se aplicável)"
    )
    
    placa = models.CharField(
        max_length=10,
        verbose_name="Placa",
        blank=True
    )
    
    renavam = models.CharField(
        max_length=11,
        verbose_name="Renavam",
        blank=True
    )
    
    ano_fabricacao = models.IntegerField(
        verbose_name="Ano de Fabricação",
        blank=True,
        null=True
    )
    
    ipva_multa = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        choices=ipva_multa_choices,
        verbose_name="IPVA/Multa"
    )
    
    video_tutorial = models.FileField(
        upload_to='tutoriais/%Y/%m/',
        verbose_name="Vídeo Tutorial",
        blank=True,
        null=True,
        help_text="Faça upload de um vídeo tutorial (MP4, AVI, MOV - máx 100MB)"
    )
    
    usuario = models.CharField(
        max_length=100,
        verbose_name="Usuário",
        blank=True
    )
    
    senha = models.CharField(
        max_length=100,
        verbose_name="Senha",
        blank=True,
        help_text="Considere usar criptografia para armazenar senhas"
    )
    
    whatsapp_confirmacao = models.CharField(
        max_length=20,
        verbose_name="WhatsApp para Confirmação de Pagamento",
        blank=True,
        help_text="Formato: (00) 00000-0000"
    )

    whatsapp_contato_alerta = models.CharField(
        max_length=20,
        verbose_name="WhatsApp para Contato de Alerta",
        blank=True,
        help_text="Formato: (00) 00000-0000"
    )
    
    link_acesso_pagamento = models.URLField(
        max_length=500,
        verbose_name="Link de Acesso ao Pagamento",
        blank=True
    )
    
    # Observações
    descricao_observacao = models.TextField(
        verbose_name="Descrição ou Observação",
        blank=True
    )
    
    # Controle de pagamento
    pago = models.BooleanField(
        default=False,
        verbose_name="Pago"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='em_dia',
        blank=True,
        verbose_name="Status da Conta"
    )
    
    data_pagamento = models.DateField(
        verbose_name="Data de Pagamento",
        blank=True,
        null=True
    )
    
    # Metadados
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Conta a Pagar"
        verbose_name_plural = "Contas a Pagar"
        ordering = ['-data_vencimento']
        indexes = [
            models.Index(fields=['data_vencimento', 'pago']),
            models.Index(fields=['grupo_conta', 'data_vencimento']),
        ]
    
    def __str__(self):
        return f"{self.nome_conta} - R$ {self.valor} - {self.data_vencimento.strftime('%d/%m/%Y')}"
    
    def is_vencida(self):
        """Verifica se a conta está vencida"""
        from django.utils import timezone
        return not self.pago and self.data_vencimento < timezone.now().date()
    
    def dias_vencimento(self):
        """Retorna quantos dias faltam para o vencimento (negativo se vencida)"""
        from django.utils import timezone
        delta = self.data_vencimento - timezone.now().date()
        return delta.days


class Faturamento(models.Model):
    """Controle de faturamento mensal"""
    
    mes_referencia = models.DateField(
        verbose_name="Mês de Referência",
        help_text="Primeiro dia do mês de referência"
    )
    
    FaturamentoLoja = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Valor do Faturamento Loja"
    )

    FaturamentoModoBank_PIX = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Valor do Faturamento ModoBank PIX"
    )

    FaturamentoModoBank_Cartao = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Valor do Faturamento ModoBank Cartão"
    )

    FaturamentoEfiBank_Boleto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Valor do Faturamento EfiBank Boleto"
    )

    FaturamentoCelcoin_Cartao = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Valor do Faturamento Celcoin Cartão"
    )

    FaturamentoMaquinaCartao = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Valor do Faturamento Maquina Cartão"
    )

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Valor do Faturamento Bruto Total"
    )
    
    observacao = models.TextField(
        verbose_name="Observação",
        blank=True
    )
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Faturamento"
        verbose_name_plural = "Faturamentos"
        ordering = ['-mes_referencia']
        indexes = [
            models.Index(fields=['mes_referencia']),
        ]

    def __str__(self):
        return f"Faturamento {self.mes_referencia.strftime('%m/%Y')} - R$ {self.valor}"

    @classmethod
    def get_ultimo_faturamento(cls):
        """Retorna o último faturamento registrado"""
        return cls.objects.order_by('-mes_referencia').first()
