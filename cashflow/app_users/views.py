from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView

from app_users.forms import CustomUserCreationForm, CustomUserChangeForm
from app_users.models import CustomUser
from app_users.utils import sending_calc, check_recipients


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


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = CustomUserChangeForm(instance=request.user)
        return render(request, 'users/profile.html', {'form': form})

    def post(self, request):
        if request.method == 'POST':
            form = CustomUserChangeForm(instance=request.user, data=request.POST)
            if form.is_valid():
                form.save()
        return redirect('user_profile_url')


class MoneySendView(LoginRequiredMixin, View):
    def post(self, request):
        if request.user.is_staff:
            sender_tin = request.POST['sender']
            sender = CustomUser.objects.filter(tin=sender_tin).first()
        else:
            sender = request.user

        amount = float(request.POST['sum'])  # проверка на число реализована в input pattern
        recipients = request.POST.getlist('recipients')

        status_recipients = check_recipients(recipients=recipients, sender=sender)

        if status_recipients is True:
            cashflow = sending_calc(sender=sender, amount=amount, recipients=recipients)
            return render(request, 'success.html', context={'content': cashflow})
        else:
            return render(request, 'success.html', context={'content': status_recipients})

    def get(self, request):
        if request.user.is_staff:
            senders = CustomUser.objects.all()
            recipients = CustomUser.objects.all().exclude(id__exact=request.user.id)
            return render(request, 'send.html', context={'recipients_list': recipients, 'senders_list': senders})
        else:
            recipients = CustomUser.objects.all().filter(is_staff=False).exclude(id__exact=request.user.id)
            return render(request, 'send.html', context={'recipients_list': recipients})
