from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from allauth.account.forms import SignupForm
from allauth.account.views import SignupView
from .forms import TaskForm
from .models import Task, TaskLog

@login_required
def update_status_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    task.status = 'concluida'
    task.save()

    task_log = TaskLog.objects.filter(task=task).first()

    if task_log:
        task_log.message = 'Status atualizado'
        task_log.save()
    else:
        TaskLog.objects.create(task=task, message='Status atualizado')

    return redirect('list:home')

def edit_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('list:home')
    else:
        form = TaskForm(instance=task)

    context = {
        'form': form,
        'task': task
    }

    return render(request, 'taskedit.html', context)

@login_required
def delete_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # Excluir o registro de log associado à tarefa (se existir)
    TaskLog.objects.filter(task=task).delete()

    task.delete()

    return redirect('list:home')

class CustomSignupView(SignupView):
    form_class = SignupForm
    template_name = 'register.html'
    success_url = '/list/'

@login_required
def home_view(request):
    user = request.user
    tasks = Task.objects.filter(user=user).order_by('-tasklog__created_at')
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
            return redirect('/list/')
        else:
            print('Usuário não encontrado ou senha incorreta.')

    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            try:
                form.save(request=request)
                print('Usuário registrado com sucesso.')
                return redirect('/list/')
            except Exception as e:
                print(f'Erro no registro do usuário: {str(e)}')
        else:
            print('Formulário inválido.')
            print(form.errors)
    else:
        form = SignupForm()

    return render(request, 'register.html', {'form': form})
