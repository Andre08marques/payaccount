from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.pay.models import ContaPagar


class Command(BaseCommand):
    help = 'Verifica e atualiza o status das contas conforme proximidade do vencimento'

    def handle(self, *args, **options):
        hoje = timezone.now().date()
        
        # Atualizar para 'Próximo a Vencer'
        contas_em_dia = ContaPagar.objects.filter(
            status='em_dia',
            pago=False
        )
        
        contas_prox_vencer = 0
        for conta in contas_em_dia:
            dias_ate_vencimento = (conta.data_vencimento - hoje).days
            
            if dias_ate_vencimento <= conta.alertar_dias_antes and dias_ate_vencimento > 0:
                conta.status = 'prox_vencer'
                conta.save(update_fields=['status', 'atualizado_em'])
                contas_prox_vencer += 1
        
        # Atualizar para 'Vence Hoje'
        contas_vence_hoje = ContaPagar.objects.filter(
            data_vencimento=hoje,
            pago=False,
            status__in=['em_dia', 'prox_vencer']
        ).update(status='vence_hoje')
        
        # Atualizar para 'Em Atraso'
        contas_atrasadas = ContaPagar.objects.filter(
            data_vencimento__lt=hoje,
            pago=False
        ).exclude(status='atrasado').update(status='atrasado')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Status atualizado:\n'
                f'- {contas_prox_vencer} contas marcadas como "Próximo a Vencer"\n'
                f'- {contas_vence_hoje} contas marcadas como "Vence Hoje"\n'
                f'- {contas_atrasadas} contas marcadas como "Em Atraso"'
            )
        )
