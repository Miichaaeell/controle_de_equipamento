from django.views.generic import View, DetailView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from datetime import datetime


class LoginView(View):
    hour = datetime.now().time().hour
    if hour > 0 and hour < 12:
        saudacao = 'Bom dia'
    elif hour >= 12 and hour < 18:
        saudacao = 'Boa Tarde'
    elif hour >= 18 and hour <= 23:
        saudacao = 'Boa Noite'

    def get(self, request, *args, **kwargs):
        context = {
            'saudacao': self.saudacao
        }
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.has_perm('controller_stock.view_controllerstock') and user.has_perm('controller_stock.add_controllerstock'):
                return redirect('dashboard')
            else:
                return redirect('stock')

        else:
            context = {
                'saudacao': self.saudacao,
                'erro': 'Usuário ou Senha inválidos'
            }
            return render(request, 'login.html', context)


class LogoutView(View):
    def get(self, request, *args, **Kwargs):
        logout(request)
        return redirect('login')


class DetailAccountView(DetailView):
    model = User
    template_name = 'detail_account.html'


class PasswordChangeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'change_password.html')

    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        old_password = request.POST['old_password']
        validation_password = user.check_password(old_password)
        if validation_password:
            new_password = request.POST['new_password']
            confirmation_password = request.POST['confirmation_passowrd']
            if new_password == confirmation_password:
                user.set_password(new_password)
                user.save()
                return redirect('logout')
            else:
                context = {
                    'error': 'As senhas não são iguais'
                }
                return render(request, 'change_password.html', context)
        else:
            context = {
                'erro': 'Senha atual não confere'
            }
            return render(request, 'change_password.html', context)
