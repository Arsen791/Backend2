from django.forms import Form, ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group 
from django import forms
class UserLoginForm(Form):
    username = forms.CharField(required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}))
    password = forms.CharField(required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Enter your password'}))
    
class RegistrationForm(ModelForm):

	repeat_password = forms.CharField(min_length=8, max_length=20, required=True, widget=
                        forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repeat your password'}))
	
	group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label='Choose Group')

	def clean_repeat_password(self):
		password1 = self.cleaned_data.get("password")
		password2 = self.cleaned_data.get("repeat_password")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords do not match")
		return password2

	class Meta:
			model = User
			fields = {'username', 'password', 'group'}
			widgets = {
				'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
				'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
			}
	
	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data["password"])
		if commit:
			user.save()
		return user