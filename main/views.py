from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.handlers.wsgi import WSGIRequest
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from main.forms import IndexLoginForm, RegisterForm
from main.models import Session, User
from jadiinbot.settings import SERVER_URL
import requests as r

class IndexView(View):
    def get(self, request: WSGIRequest):
        if request.user.is_authenticated:
            return redirect('dashboard')

        return render(request, 'main/index.html')

    def post(self, request: WSGIRequest):
        if request.user.is_authenticated:
            return redirect('dashboard')
            
        form = IndexLoginForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest('Bad Request')

        user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
        if not user:
            context = {
                'error_msg': 'Kombinasi username dan password tidak cocok!'
            }
            return render(request, 'main/index.html', context)
        
        login(request, user)
        return redirect('dashboard')


@method_decorator(login_required, name = 'dispatch')
class DashboardView(View):
    def get(self, request: WSGIRequest):
        session = Session.objects.filter(owner__id = request.user.id).first()
        if not session:
            sessid = request.COOKIES.get('sessionid')
            context = {
                'session_id': sessid,
            }
            return render(request, 'main/dashboard.html', context)
        else:
            data = r.get(SERVER_URL + 'conn/' + str(request.user.id)).json()
            sessid = request.COOKIES.get('sessionid')
            context = data['data'].copy()
            context['session_id'] = sessid
            return render(request, 'main/dashboard_has_connect.html', context)


class RegisterView(View):
    def get(self, request: WSGIRequest):
        if request.user.is_authenticated:
            return redirect('dashboard')

        return render(request, 'main/register.html')

    def post(self, request: WSGIRequest):
        if request.user.is_authenticated:
            return redirect('dashboard')
            
        form = RegisterForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest('Bad Request')
        
        if not form.cleaned_data['username'].isalnum():
            context = {
                'error_msg': 'Username hanya mendukung alphanumeric'
            }
            return render(request, 'main/register.html', context)

        if len(form.cleaned_data['password']) < 5 or len(form.cleaned_data['password']) > 20:
            context = {
                'error_msg': 'Password minimal 5 karakter, maksimal 20 karakter'
            }
            return render(request, 'main/register.html', context)

        if User.objects.filter(username = form.cleaned_data['username'].lower()).first():
            context = {
                'error_msg': 'Username sudah ada'
            }
            return render(request, 'main/register.html', context)
        
        if form.cleaned_data['password'] != form.cleaned_data['confirm_password']:
            context = {
                'error_msg': 'Password dan konfirmasi password tidak sama'
            }
            return render(request, 'main/register.html', context)
        
        
        user = User.objects.create_user(
            username = form.cleaned_data['username'].lower(),
            password = form.cleaned_data['password']
        )
        user.save()
        login(request, user)
        return redirect('dashboard')