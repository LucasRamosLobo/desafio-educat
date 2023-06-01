from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from allauth.account.forms import SignupForm
from allauth.account.views import SignupView
from .forms import TaskForm
from .models import Task, TaskLog

def update_status_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # Atualize o status da tarefa como necessário
    task.status = 'concluida'  # Altere para o status desejado
    task.save()

    # Verifique se já existe um registro de log para a tarefa
    task_log = TaskLog.objects.filter(task=task).first()

    if task_log:
        # Atualize o registro de log existente
        task_log.message = 'Status atualizado'
        task_log.save()
    else:
        # Crie um novo registro de log
        TaskLog.objects.create(task=task, message='Status atualizado')

    return redirect('list:home')

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
                form.save(request=request)
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
