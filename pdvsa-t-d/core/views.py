from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login


class Login(TemplateView):
    template_name = "login.html"

    def get(self, request, *args, **kwargs):
        if not request.user.is_anonymous():
            return HttpResponseRedirect('/control')
        return TemplateView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        next = request.GET.get('next', '')
        if next == '':
            next = '/control'
        username = request.POST.get('inputUser', '')
        password = request.POST.get('inputPassword', '')
        if username != '' and password != '':
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(next)
        return HttpResponseRedirect('/Login')


@login_required(login_url='Login')
def PDVSALogout(request):
    logout(request)
    return HttpResponseRedirect('/Login')
