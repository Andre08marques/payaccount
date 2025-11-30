from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.models import User as CustomUser
from django.views import View
from .forms import CustomUserCreationForm, UserChangeForm


@method_decorator(login_required(login_url='login'), name='dispatch')
class UserList(View):
    
    def get(self, request):
        usr = CustomUser.objects.all()
        context = {
            "users": usr
        }
        return render(request, "usuarios/user_list.html", context)
      
@method_decorator(login_required(login_url='login'), name='dispatch')
class UserAdd(View):

    def get(self, request):
        form = CustomUserCreationForm()
        context = {
            "page_title": "Adicionar Usuário",
            "form": form
        }
        return render(request, "usuarios/user_add.html", context)
    
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuário cadastrado com sucesso")
            return redirect("userlist")
        messages.success(request, f"Não foi possível cadastrar o usuário. Erro: {form.errors}")
        return redirect("userlist")

@method_decorator(login_required(login_url='login'), name='dispatch')
class UserEdit(View):

    def get(self, request, id):
        user = CustomUser.objects.get(pk=id)
        form = UserChangeForm(request.POST or None, request.FILES or None, instance=user)
        context = {
            "page_title": "Editar Usuário",
            "form": form
        }
        return render(request, "usuarios/user_edit.html", context)
    
    def post(self, request, id):
        user = CustomUser.objects.get(pk=id)
        form = UserChangeForm(request.POST or None, request.FILES or None, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuário editado com sucesso")
            return redirect("userlist")
        messages.success(request, f"Não foi possível editar o usuário. Erro: {form.errors}")
        return redirect("userlist")

@method_decorator(login_required(login_url='login'), name='dispatch')
class UserDelete(View):

    def get(self, request, id):
       customuser = CustomUser.objects.get(pk=id)
       customuser_delete = customuser.delete()
       return redirect('userlist')


@method_decorator(login_required(login_url='login'), name='dispatch')
class UserChangePassword(View):
    def get(self, request, id):
        perfil = CustomUser.objects.get(pk=id)
        context = {
            'page_title': 'Reset Password',
            'perfil': perfil
        }
        return render(request, "usuarios/change_password.html", context)
    
    def post(self, request, id):

        new_password = request.POST["senha"]
        user = CustomUser.objects.get(pk=id)
        user.set_password(new_password)
        user.save()
        messages.success(request,'Senha alterada com sucesso')
        return redirect('userlist')
    