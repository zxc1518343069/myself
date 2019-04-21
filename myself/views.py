from django.shortcuts import render,redirect
from django.contrib import auth
from django.urls import reverse
from .forms import LoginForm,RegForm
from django.contrib.auth.models import User
def home(request):
    context = {}
    return render(request,'home.html', context)

def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request,user)
            if user is not None:
                auth.login(request,user)
                return redirect(request.GET.get('from',reverse('home')))
            else:
                login_form.add_error(None,'用户名或者密码不正确')
    else:
        login_form = LoginForm()
    context = {}
    context['login_form'] = login_form
    return render(request,'login.html',context)
def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            #注册
            username = reg_form.cleaned_data['username']
            password = reg_form.cleaned_data['password']
            email = reg_form.cleaned_data['email']
            # 创建用户
            user = User.objects.create_user(username=username,password=password,email=email)
            user.save()
            # 登陆用户
            '''
            user = User
            user.email = email
            user.set_password(password)
            user.username = username
            user.save()
            '''
            user = auth.authenticate(username=username, password=password)
            auth.login(request,user)
            return redirect(request.GET.get('from',reverse('home')))
    else:
        reg_form = RegForm()

    context = {}
    context['reg_form'] = reg_form
    return render(request,'register.html',context)
