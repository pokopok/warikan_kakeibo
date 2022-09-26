from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from .models import Expenses
from warikan.models import Expenses
from .forms import UserLoginForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

class HomeView(TemplateView):
    template_name = 'home.html'


# ログイン・ログアウト機能
class LoginView(LoginView):
    template_name = 'login.html'
    authentication_form = UserLoginForm

class LogoutView(LogoutView):
    pass

# 支出入力画面
class ExpensesAddView(LoginRequiredMixin, CreateView):
    model = Expenses
    fields = ['date', 'payer', 'category', 'price', 'memo']
    template_name = 'expenses_add.html'

    def get_success_url(self):
        form = super(ExpensesAddView, self).get_form()
        return reverse('warikan:home')

    def form_valid(self, form): #フォーム送信前に実行される
        form.instance.user = self.request.user
        return super(ExpensesAddView, self).form_valid(form)

    def get_form(self):
        form = super(ExpensesAddView, self).get_form()
        form.fields['date'].label = '日付'
        form.fields['payer'].label = '支払者'
        form.fields['category'].label = 'カテゴリー'
        form.fields['price'].label = '金額'
        form.fields['memo'].label = 'メモ'
        return form