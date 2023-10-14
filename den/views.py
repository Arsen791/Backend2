from django.shortcuts import render, redirect
import random
import math
from den.models import Problem, Action
from den.form import ProblemForm, ActionForm, ProblemDetailForm, ProblemDetailForm2, Problem_assigned_userForm
from django.contrib.auth.models import Group
from django.http.response import HttpResponse
from django.contrib.auth.models import User



def create_problem(request):
        if request.method == 'GET':
            problem_form = ProblemForm()
            return render(request, 'create-name.html', {'form': problem_form})
        if request.method == 'POST':
            problem_form = ProblemForm(request.POST)
            if problem_form.is_valid():
                firstname = problem_form.data.get('firstname')
                number = problem_form.data.get('number')
                email = problem_form.data.get('email')
                problems = problem_form.data.get('problems')
                priority = problem_form.data.get('priority')
                status = problem_form.data.get('status')

                reception_group = Group.objects.get(name='Reception')
                reception_user = reception_group.user_set.first()
                
                problem = Problem(firstname=firstname, number=number, email=email, problems=problems, priority=priority, status=status)
                problem.assigned_user = reception_user
                problem.save()
                return redirect('/')
            else:
                return render(request, 'create-name.html', {'form': problem_form})
            


def user_action(request, pk):
    if request.user.is_authenticated:
        problem = Problem.objects.get(id=pk)
        if request.method == 'POST':
            action_form = ActionForm(request.POST)
            assigned_form = Problem_assigned_userForm(request.POST)
            problem_detail_form = ProblemDetailForm(request.POST)
            problem_detail_form2 = ProblemDetailForm2(request.POST)
            user_is_reception = request.user.groups.filter(name='Reception').exists()
            user_is_tester = request.user.groups.filter(name='Tester').exists()
            if user_is_reception:
                if action_form.is_valid() and problem_detail_form.is_valid() and assigned_form.is_valid():
                    actions = action_form.data.get('action')
                    user_action = Action(action=actions, id=problem.id, user_name=problem)
                    user_action.save()
                    status = problem_detail_form.cleaned_data['status']
                    assigned_user = assigned_form.cleaned_data['assigned_user']
                    problem.assigned_user = assigned_user
                    problem.status = status
                    tester_group = Group.objects.get(name='Tester')
                    tester_user = tester_group.user_set.first()
                    if problem.status == 'Resolved':
                        problem.resolved_user = problem.assigned_user
                        problem.assigned_user = tester_user
                    else:
                        problem.assigned_user = problem.assigned_user
                    problem.save()

                    return redirect('/problems')
                else:
                    return redirect('/')
            elif user_is_tester:
                if action_form.is_valid() and problem_detail_form2.is_valid() and assigned_form.is_valid():
                    actions = action_form.data.get('action')
                    user_action = Action(action=actions, id=problem.id, user_name=problem)
                    user_action.save()                 
                    status2 = problem_detail_form2.cleaned_data['status']
                    assigned_user = assigned_form.cleaned_data['assigned_user']
                    problem.assigned_user = assigned_user
                    problem.status = status2
                    tester_group = Group.objects.get(name='Tester')
                    tester_user = tester_group.user_set.first()
                    if problem.status == 'Resolved':
                        problem.resolved_user = problem.assigned_user
                        problem.assigned_user = tester_user
                    else:
                        problem.assigned_user = problem.assigned_user
                    problem.save()

                    return redirect('/problems')
                else:
                    return redirect('/')
    else:
        return redirect('/auth/login/')

            

def view_problems(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            user = request.user
            problems = Problem.objects.filter(assigned_user=user)
            user_actions = Action.objects.select_related('user_name').all()
            return render(request, 'view_problem.html', {'problems': problems, 'user_actions': user_actions})
    else:
        return redirect('/auth/login/')


def user_poblem_details(request, pk):
    if request.user.is_authenticated:
        if request.method == 'GET':
            problem = Problem.objects.get(id=pk)
            user_action = Action.objects.filter(user_name_id=pk).order_by('user_name')
            first_action = user_action.first()
            if first_action:
                initial_action_value = first_action.action
            else:
                initial_action_value = ""
            action_form = ActionForm(initial={'action': initial_action_value})
            first_assigned = problem.assigned_user
            if first_action:
                initial_action_value = first_assigned
            else:
                initial_action_value = ""
            assigned_form = Problem_assigned_userForm(initial={'assigned_user': initial_action_value})
            problem_detail_form = ProblemDetailForm()
            problem_detail_form2 = ProblemDetailForm2()
            user_is_reception = request.user.groups.filter(name='Reception').exists()
            user_is_tester = request.user.groups.filter(name='Tester').exists()
            return render(request, 'detail_problems.html', {'problems': problem, 'form3':assigned_form, 'user_actions': user_action, 'form': action_form , 'form1': problem_detail_form, 'form2':problem_detail_form2, 'user_is_reception':user_is_reception, 'user_is_tester':user_is_tester})
    else:
        return redirect('/auth/login/')




def radius(request) :
    if request.method == 'POST':
        rad = request.POST.get('rad')
        ad = math.sin(float(rad))
        return render(request, "index.html", {"ad": ad})
    
    return render(request, "index.html",)

def asu(request):
    if 'random_number' not in request.session:
        request.session['random_number'] = random.randint(1, 100)

    random_number = request.session['random_number']
	
    if request.method == 'POST':
        rad = int(request.POST.get('rad'))
        ase = ''
        if rad < random_number:
            ase = "Больше"   
        elif rad > random_number:
            ase = "Меньше"
        elif rad == random_number:
            ase = "Нашли"
            request.session['random_number'] = random.randint(1, 100)
        return render(request, "asu.html", {"ase": ase})
  
    return render(request, "asu.html")



