from django.contrib import admin
from .models import Faturamento

# Register your models here.

@admin.register(Faturamento)
class FaturamentoAdmin(admin.ModelAdmin):
    list_display = ['mes_referencia', 'valor', 'criado_em']
    list_filter = ['mes_referencia']
    search_fields = ['observacao']
    date_hierarchy = 'mes_referencia'
