from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import ContaPagar
from django.conf import settings
from main.src.agents.evolution_agent import Evolution


@shared_task
def enviar_confirmacao_pagamento(conta_id, data_pagamento_str):
    """
    Task para enviar confirmação de pagamento via WhatsApp em segundo plano.
    
    Args:
        conta_id: ID da conta que foi paga
        data_pagamento_str: Data do pagamento no formato 'YYYY-MM-DD'
    """
    try:
        conta = ContaPagar.objects.get(id=conta_id)
        
        # Verificar se tem WhatsApp e mensagem configurados
        if not conta.whatsapp_confirmacao or not conta.mensagem_confirmacao:
            return f"Conta {conta_id}: WhatsApp ou mensagem não configurados"
        
        ev = Evolution()
        
        # Converter string de data para objeto date
        from datetime import datetime
        data_pagamento = datetime.strptime(data_pagamento_str, '%Y-%m-%d').date()
        
        # Formatar mensagem substituindo variáveis
        mensagem = conta.mensagem_confirmacao
        mensagem = mensagem.replace('{{nome_conta}}', conta.nome_conta)
        mensagem = mensagem.replace('{{valor}}', f"R$ {conta.valor}")
        mensagem = mensagem.replace('{{data_pagamento}}', data_pagamento.strftime('%d/%m/%Y'))
        
        # Enviar via WhatsApp
        response = ev.instance_send_text(
            settings.INSTANCE_NAME,
            settings.INSTANCE_KEY,
            conta.whatsapp_confirmacao,
            mensagem
        )
        
        return f"Confirmação enviada para {conta.whatsapp_confirmacao} - Conta: {conta.nome_conta}"
        
    except ContaPagar.DoesNotExist:
        return f"Erro: Conta {conta_id} não encontrada"
    except Exception as e:
        return f"Erro ao enviar confirmação para conta {conta_id}: {str(e)}"


@shared_task
def verificar_status_contas():
    """
    Task periódica para atualizar o status das contas conforme proximidade do vencimento.
    Executa diariamente para verificar contas que precisam de alerta.
    """
    hoje = timezone.now().date()
    contas_atualizadas = 0
    ev = Evolution()
    
    # Buscar contas em dia e não pagas
    contas = ContaPagar.objects.filter(
        status='em_dia',
        pago=False
    )
    
    for conta in contas:
        dias_ate_vencimento = (conta.data_vencimento - hoje).days
        
        # Se os dias até o vencimento são menores ou iguais ao alerta configurado
        if dias_ate_vencimento <= conta.alertar_dias_antes and dias_ate_vencimento > 0:
            conta.status = 'prox_vencer'
            conta.save(update_fields=['status', 'atualizado_em'])
            
            # Enviar alerta apenas se houver WhatsApp configurado
            if conta.whatsapp_contato_alerta:
                # Formatar mensagem de alerta
                mensagem = (
                    "⚠️ ATENÇÃO! ⚠️\n\n"
                    "A Conta Abaixo Está Próxima a Vencer.\n\n"
                    f"Vencimento: {conta.data_vencimento.strftime('%d/%m/%Y')}\n\n"
                    f"Nome da Conta: {conta.nome_conta}\n\n"
                    "👉 Verifique o Pagamento Para Evitar Transtornos."
                )
                
                # Enviar alerta via WhatsApp
                response = ev.instance_send_text(
                    settings.INSTANCE_NAME,
                    settings.INSTANCE_KEY,
                    conta.whatsapp_contato_alerta,
                    mensagem
                )
            
            contas_atualizadas += 1
    
    return f"{contas_atualizadas} contas atualizadas para 'Próximo a Vencer'"


@shared_task
def verificar_contas_vencendo_hoje():
    """
    Task para marcar contas que vencem hoje.
    """
    hoje = timezone.now().date()
    ev = Evolution()
    
    contas_vencendo_hoje = ContaPagar.objects.filter(
        data_vencimento=hoje,
        pago=False,
        status__in=['em_dia', 'prox_vencer']
    )
    
    contas_atualizadas = 0
    for conta in contas_vencendo_hoje:
        conta.status = 'vence_hoje'
        conta.save(update_fields=['status', 'atualizado_em'])
        
        # Enviar alerta apenas se houver WhatsApp configurado
        if conta.whatsapp_contato_alerta:
            # Formatar mensagem de alerta
            mensagem = (
                "🚨 ATENÇÃO! 🚨\n\n"
                "A Conta Abaixo a Vencer Hoje.\n\n"
                f"Vencimento: {conta.data_vencimento.strftime('%d/%m/%Y')}\n\n"
                f"Nome da Conta: {conta.nome_conta}\n\n"
                "👉 Verifique o Pagamento Para Evitar Transtornos."
            )
            
            # Enviar alerta via WhatsApp
            response = ev.instance_send_text(
                settings.INSTANCE_NAME,
                settings.INSTANCE_KEY,
                conta.whatsapp_contato_alerta,
                mensagem
            )
        
        contas_atualizadas += 1
    
    return f"{contas_atualizadas} contas atualizadas para 'Vence Hoje'"


@shared_task
def verificar_contas_atrasadas():
    """
    Task para marcar contas atrasadas.
    """
    hoje = timezone.now().date()
    
    contas_atrasadas = ContaPagar.objects.filter(
        data_vencimento__lt=hoje,
        pago=False
    ).exclude(status='atrasado')
    
    contas_atualizadas = contas_atrasadas.update(status='atrasado')
    
    return f"{contas_atualizadas} contas atualizadas para 'Em Atraso'"
