from django import forms
from django.core.exceptions import ValidationError
from .models import Matricula, Curso
from datetime import date


class MatriculaForm(forms.ModelForm):
    class Meta:
        model = Matricula
        fields = [
            'nome_completo', 'data_nascimento', 'genero', 'nacionalidade',
            'bilhete_identidade', 'telefone', 'email', 'endereco',
            'curso', 'forma_pagamento', 'observacoes'
        ]
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'endereco': forms.Textarea(attrs={'rows': 3}),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'nome_completo': 'Nome completo',
            'data_nascimento': 'Data de nascimento',
            'genero': 'Gênero',
            'nacionalidade': 'Nacionalidade',
            'bilhete_identidade': 'BI/NUIT',
            'telefone': 'Telefone (com código)',
            'email': 'E-mail',
            'endereco': 'Endereço',
            'curso': 'Curso pretendido',
            'forma_pagamento': 'Forma de pagamento',
            'observacoes': 'Observações (opcional)',
        }

    def clean_data_nascimento(self):
        data = self.cleaned_data['data_nascimento']
        idade = (date.today() - data).days // 365
        if idade < 14:
            raise ValidationError('O aluno deve ter pelo menos 14 anos.')
        return data

    def clean_bilhete_identidade(self):
        bi = self.cleaned_data['bilhete_identidade']
        # Verifica se já existe matrícula com esse BI
        if Matricula.objects.filter(bilhete_identidade=bi).exists():
            raise ValidationError('Já existe uma matrícula com este BI/NUIT.')
        return bi