from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

Usuario = get_user_model()


class CadastroUsuarioForm(UserCreationForm):
    perfil = forms.ChoiceField(
        choices=[
            (Usuario.Perfil.ALUNO, 'Aluno'),
            (Usuario.Perfil.PROFESSOR, 'Professor'),
        ],
        label='Perfil',
    )

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'perfil',
        )
        labels = {
            'username': 'Nome de usuário',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for campo in (
            'first_name',
            'last_name',
            'email',
        ):
            self.fields[campo].required = True

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()

        if Usuario.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                'Este e-mail já está cadastrado.'
            )

        return email

    def clean_perfil(self):
        perfil = self.cleaned_data['perfil']

        if perfil not in (
            Usuario.Perfil.ALUNO,
            Usuario.Perfil.PROFESSOR,
        ):
            raise forms.ValidationError(
                'Perfil inválido para cadastro público.'
            )

        return perfil
