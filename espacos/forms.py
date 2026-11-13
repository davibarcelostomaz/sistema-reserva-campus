from django import forms
from .models import Espaco


class EspacoForm(forms.ModelForm):

    class Meta:
        model = Espaco
        fields = ['nome', 'tipo', 'capacidade', 'recursos', 'localizacao']