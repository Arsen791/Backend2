from django.forms import Form
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

class Problem_assigned_userForm(Form):
    assigned_user = forms.ModelChoiceField(
        queryset= User.objects.filter(groups__isnull=False, is_superuser=False),
        required=False, 
        widget=forms.Select(attrs={'readonly': 'readonly', 'id': 'id_status'}),  # Добавьте класс для стилизации виджета
    )

class ProblemDetailForm(Form):
    STATUS_CHOICES = [
        ('NEW', 'NEW'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),


    ]
    status = forms.ChoiceField(choices=STATUS_CHOICES, initial='NEW', widget=forms.Select)

class ProblemDetailForm2(Form):
    STATUS_CHOICES = [
        ('NEW', 'NEW'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Confirmed', 'Confirmed'),

    ]
    status = forms.ChoiceField(choices=STATUS_CHOICES, initial='NEW', widget=forms.Select)


class ProblemForm(Form):
    firstname = forms.CharField(required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}))
    number = forms.IntegerField(required=True,
                               widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Enter your number', 'type':'number'}))
    email = forms.EmailField(required=True,
                               widget=forms.EmailInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Enter your email ', 'type':'email'}))
    problems = forms.CharField(required=True,
                               widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your problem', 'type':'text'}))
    CHOICES = [
        ('Низкий', 'Низкий'),
        ('Средний', 'Средний'),
        ('Высокий', 'Высокий'),
	]
    priority = forms.ChoiceField(choices=CHOICES, initial='Низкий', widget=forms.Select)

    STATUS_CHOICES = [
        ('NEW', 'NEW'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        

    ]
    status = forms.ChoiceField(choices=STATUS_CHOICES, initial='NEW', widget=forms.Select(attrs={'readonly': 'readonly', 'id': 'id_status'}))

    assigned_user = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='Reception'),
        required=False, 
        widget=forms.Select(attrs={'readonly': 'readonly', 'id': 'id_status'}),
    )

    
class ActionForm(Form):
    action = forms.CharField(required=False,
                               widget=forms.TextInput(attrs={'id': 'action'}))
