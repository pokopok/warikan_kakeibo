from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from .models import Expenses
from warikan.models import Expenses
from .forms import UserLoginForm, ExpensesSearchForm
from django.contrib.auth.views import LoginView, LogoutView
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

class ExpensesListView(LoginRequiredMixin, ListView):
    model = Expenses
    template_name = 'expenses_list.html'
    ordering = '-date'

    def get_queryset(self):
        qs = super(ExpensesListView, self).get_queryset()
        self.form = form = ExpensesSearchForm(self.request.GET or None)

        if form.is_valid():
            # 年での絞り込み
            year = form.cleaned_data.get('year')
            if year and year != '0':
                qs = qs.filter(date__year=year)

            # 月での絞り込み
            month = form.cleaned_data.get('month')
            if month and month != '0':
                qs = qs.filter(date__month=month)
            
            # キーワードでの絞り込み
            key_word = form.cleaned_data.get('key_word')
            if key_word:
                # 空欄で区切り、順番に絞る、and検索
                if key_word:
                    for word in key_word.split():
                        qs = qs.filter(memo__icontains=word)
            
            # カテゴリでの絞り込み
            category = form.cleaned_data.get('category')
            if category:
                qs = qs.filter(category=category)
            
            # 支払者での絞り込み
            payer = form.cleaned_data.get('payer')
            if payer:
                qs = qs.filter(payer=payer)
        
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.form
        
        return context


class MonthDashboard(TemplateView):
    template_name = 'month_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = int(self.kwargs.get('year'))
        month = int(self.kwargs.get('month'))

        # 前月と次月を設定
        if month == 1:
            pre_month_year = year - 1
            pre_month_month = 12
        else:
            pre_month_year = year
            pre_month_month = month - 1
        
        if month == 12:
            next_month_year = year + 1
            next_month_month = 1
        else:
            next_month_year = year
            next_month_month = month + 1

        context['year_month'] = f'{year}年{month}月'
        context['pre_month_year'] = pre_month_year
        context['pre_month_month'] = pre_month_month
        context['next_month_year'] = next_month_year
        context['next_month_month'] = next_month_month

        return context