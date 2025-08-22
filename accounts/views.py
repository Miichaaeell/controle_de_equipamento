from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# Create your views here.


class LoginView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'saudacao': 'Bom dia'
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
                'saudacao': 'Bom dia',
                'erro': 'Usuário ou Senha inválidos'
            }
            return render(request, 'login.html', context)


class LogoutView(View):
    def get(self, request, *args, **Kwargs):
        logout(request)
        return redirect('login')
