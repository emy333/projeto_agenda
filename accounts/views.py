from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .models import FormContato
# Create your views here.

def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)
    if not user:
        print('Usuário ou senha inválidos.')
        return render(request='accounts/login.html')
    else:
        auth.login(request, user)
        print('Logado com sucesso.')
        return redirect('dashboard')

def logout(request):
    auth.logout(request)
    return redirect('index')

def cadastro(request):
    if request.method != 'POST':
        return render(request, 'accounts/cadastro.html')
    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')

    if not nome or not sobrenome or not email or not usuario or not senha or not senha2:
        print('Nenhum campo pode estar vazio.')
        return render(request, 'accounts/cadastro.html')
    
    if len(senha) < 6:
        print('Senha muito curta (Precisa ter mais de 6 caracteres).')
        return render(request, 'accounts/cadastro.html')
    
    if senha != senha2:
        print('As senhar precisam ser iguais.')
        return render(request, 'accounts/cadastro.html')


    if User.objects.filter(username=usuario).exists():
        print('Nome de usuário já existe. ')
        return render(request, 'accounts/cadastro.html')
    
    if User.objects.filter(email=email).exists():
        print('Email já existe.')
        return render(request, 'accounts/cadastro.html')

    print('Registrado com sucesso.')

    user = User.objects.create_user(username=usuario, email=email, password=senha, first_name=nome, last_name=sobrenome)
    user.save()
    return redirect('login')

@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':
        form = FormContato() 
        return render(request, 'accounts/dashboard.html', {'form': form})   
    
    form = FormContato(request.POST, request.FILES)

    if not form.is_valid():
        print('Erro ao enviar formulário')
        form = FormContato(request.POST) 
        return render(request, 'accounts/dashboard.html', {'form': form})  
    
    form.save()
    print('Sucessso')
    return redirect('dashboard')