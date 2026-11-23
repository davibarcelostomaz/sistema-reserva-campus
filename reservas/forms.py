from datetime import date

from django import forms

from .models import Reserva


class SolicitacaoReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['espaco', 'data', 'hora_inicio', 'hora_fim']

        labels = {
            'espaco': 'Espaço',
            'data': 'Data da reserva',
            'hora_inicio': 'Horário de início',
            'hora_fim': 'Horário de término',
        }

        widgets = {
            'data': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date'}
            ),
            'hora_inicio': forms.TimeInput(
                format='%H:%M',
                attrs={'type': 'time'}
            ),
            'hora_fim': forms.TimeInput(
                format='%H:%M',
                attrs={'type': 'time'}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        espaco = cleaned_data.get('espaco')
        data = cleaned_data.get('data')
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fim = cleaned_data.get('hora_fim')

        # Impede reservas em datas passadas.
        if data and data < date.today():
            self.add_error(
                'data',
                'Não é possível reservar uma data passada.'
            )

        # O horário final deve ser posterior ao inicial.
        if hora_inicio and hora_fim and hora_inicio >= hora_fim:
            self.add_error(
                'hora_fim',
                'O horário de término deve ser posterior ao início.'
            )

        # Verifica conflitos somente quando os campos são válidos.
        if (
            espaco
            and data
            and hora_inicio
            and hora_fim
            and not self.errors
        ):
            conflitos = Reserva.objects.filter(
                espaco=espaco,
                data=data,
                hora_inicio__lt=hora_fim,
                hora_fim__gt=hora_inicio,
                status__in=[
                    Reserva.Status.PENDENTE,
                    Reserva.Status.APROVADA,
                ],
            )

            # Evita conflito com a própria reserva em uma edição.
            if self.instance.pk:
                conflitos = conflitos.exclude(pk=self.instance.pk)

            if conflitos.exists():
                raise forms.ValidationError(
                    'Este espaço já possui uma reserva nesse '
                    'intervalo de horário. Escolha outro horário.'
                )

        return cleaned_data