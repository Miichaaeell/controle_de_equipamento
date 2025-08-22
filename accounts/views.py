from django.views.generic import View
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
            return redirect('dashboard')

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
