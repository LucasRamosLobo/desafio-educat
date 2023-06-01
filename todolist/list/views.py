from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from allauth.account.forms import SignupForm
from allauth.account.views import SignupView
from .forms import TaskForm
from .models import Task, TaskLog

class CustomSignupView(SignupView):
    form_class = SignupForm
    template_name = 'register.html'
    success_url = '/list/'

@login_required
def home_view(request):
    user = request.user
    tasks = Task.objects.filter(user=user).order_by('-tasklog__created_at')  # Ordena as tarefas pelo campo created_at do modelo TaskLog
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = user
            task.save()
            # Cria um registro de log da criação da tarefa
            TaskLog.objects.create(task=task, message='Tarefa criada')

            return redirect('list:home')

    context = {
        'user': user,
        'tasks': tasks,
        'form': form
    }

    return render(request, 'home.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(f'O usuário {username} existe.')
            return redirect('/list/')  # Redireciona para a página de sucesso após o login
        else:
            print('Usuário não encontrado ou senha incorreta.')

    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            try:
                form.save(request=request)  # Corrigido: passando o argumento request
                print('Usuário registrado com sucesso.')
                return redirect('/list/')  # Redireciona para a página de sucesso após o registro
            except Exception as e:
                print(f'Erro no registro do usuário: {str(e)}')
        else:
            print('Formulário inválido.')
            print(form.errors)  # Imprime os erros do formulário no terminal
    else:
        form = SignupForm()

    return render(request, 'register.html', {'form': form})
