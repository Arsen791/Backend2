from django.shortcuts import render, redirect
from user.forms import RegistrationForm, UserLoginForm
from django.contrib.auth.models import auth
from django.contrib.auth import login 
from django.contrib.auth.models import Group

def user_login(request):
	if request.method == 'GET':
		form = UserLoginForm()
		return render(request, 'user/login.html', {'form': form})
	if request.method == 'POST':
		form = UserLoginForm(request.POST)
		if form.is_valid():
			username = form.data.get('username')
			password = form.data.get('password')
			user = auth.authenticate(username=username, password=password)
			login(request, user)
			if user is not None:
				return redirect('/problems')
			else:
				form.add_error(field='username', error='Invalid password or login')
				return render(request, 'user/login.html', {'form': form})
	return render(request, 'user/login.html', {'form': form})


def register(request):
	if request.method == 'GET':
		form = RegistrationForm()
		return render(request, 'user/registration.html', {'form': form})
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.save()
			password = form.data.get('password')
			selected_group = form.cleaned_data.get('group')
			selected_group.user_set.add(user)
			auth_data = auth.authenticate(request, password=password)
			if auth_data is not None:
				login(request, auth_data)
				return redirect('/')
			return redirect('/auth/login/')
		else:
			return render(request, 'user/registration.html', {'form':form})
		
	