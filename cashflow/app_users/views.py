from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, UpdateView

from app_users.forms import CustomUserCreationForm, CustomUserChangeForm
from app_users.models import CustomUser
from app_users.utils import sending_calc


class UserRegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('main_url')
    template_name = 'users/register.html'

    def form_valid(self, form):
        valid = super().form_valid(form)
        login(self.request, self.object)
        return valid


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    next_page = 'main_url'


class MainPageView(TemplateView):
    template_name = 'main.html'


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'users/profile.html'



class MoneySendView(LoginRequiredMixin, View):
    http_method_names = ['get', 'post']

    def post(self, request):
        if request.user.is_staff:
            sender_tin = request.POST['sender']
            sender = CustomUser.objects.filter(tin=sender_tin).first()
        else:
            sender = request.user

        amount = request.POST['sum']  # проверка на число реализована в input pattern
        recipients = request.POST.getlist('recipients')
        cashflow = sending_calc(sender=sender, amount=amount, recipients=recipients)

        return render(request, 'success.html', context={'content': cashflow})

    def get(self, request):
        if request.user.is_staff:
            senders = CustomUser.objects.all()
            recipients = CustomUser.objects.all().exclude(id__exact=request.user.id)
            return render(request, 'send.html', context={'recipients_list': recipients, 'senders_list': senders})
        else:
            recipients = CustomUser.objects.filter(is_staff=False).exclude(id__exact=request.user.id)
            return render(request, 'send.html', context={'recipients_list': recipients})
