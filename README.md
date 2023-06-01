# desafio-educat

Aplicação desenvolvida usando Django, com utilização do django-allauth para autenticação. Foram criados modelos para tarefas (tasks) e para atualização do status de cada tarefa. A aplicação consiste em um to-do list simples, com o front-end implementado em HTML e CSS, e o banco de dados utilizado é o SQLite.

Para executar a aplicação, siga os seguintes passos:

Instale as dependências com o comando: pip install -r requirements.txt

Execute o projeto com o comando: python manage.py runserver

Para criar um usuário, utilize a URL /list/register. A senha deve obedecer certos critérios, senha de exemplo: 123Lucas83!

Para fazer login, utilize a URL /list/login ou /accounts/login/?next=%2Flist%2F.

Também é possível utilizar a conta já criada com as seguintes credenciais:

Nome de usuário: lucas

Senha: 123Lucas83!

