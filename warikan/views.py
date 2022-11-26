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
import numpy as np
import pandas as pd
from django_pandas.io import read_frame
from .plugin_plotly import GraphGenerator
from django.contrib.messages.views import SuccessMessageMixin

class HomeView(TemplateView):
    template_name = 'home.html'


# ログイン・ログアウト機能
class LoginView(LoginView):
    template_name = 'login.html'
    authentication_form = UserLoginForm

class LogoutView(LogoutView):
    pass

# 支出入力画面
class ExpensesAddView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Expenses
    fields = ['date', 'payer', 'category', 'is_warikan', 'price', 'memo']
    template_name = 'expenses_add.html'
    success_message = "支出を追加しました。"

    def get_success_url(self):
        form = super(ExpensesAddView, self).get_form()
        return reverse('warikan:expenses_add')

    def form_valid(self, form): #フォーム送信前に実行される
        form.instance.user = self.request.user
        return super(ExpensesAddView, self).form_valid(form)

    def get_form(self):
        form = super(ExpensesAddView, self).get_form()
        form.fields['date'].label = '日付'
        form.fields['payer'].label = '支払者'
        form.fields['category'].label = 'カテゴリー'
        form.fields['is_warikan'].label = '割り勘フラグ'
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

class Summarydashboard(TemplateView):
    template_name = 'month_summary_dashboard.html'

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

        # Expensesモデルをdfにする
        queryset = Expenses.objects.filter(date__year=year)
        queryset = queryset.filter(date__month=month)
        # クエリセットが何もない時はcontextを返す
        if not queryset:
            return context

        df = read_frame(queryset,
                        fieldnames=['date', 'payer', 'price', 'category' ,'is_warikan'])

        # 割り勘の数字を計算して渡す
        context['total_warikan_expenses'] = df['price'][df.is_warikan==True].sum()
        context['yusuke_warikan_expenses'] = df['price'][(df.payer=='yusuke') & (df.is_warikan==True)].sum()
        context['hinano_warikan_expenses'] = df['price'][(df.payer=='hinano') & (df.is_warikan==True)].sum()
        context['yusuke_warikan_diff'] = ((context['total_warikan_expenses'])/2-context['yusuke_warikan_expenses']).astype('int')
        context['hinano_warikan_diff'] = ((context['total_warikan_expenses'])/2-context['hinano_warikan_expenses']).astype('int')
        # 個人の合計値を計算して渡す
        context['yusuke_expenses'] = (df['price'][(df.payer=='yusuke') & (df.is_warikan==False)].sum()+(context['total_warikan_expenses'])/2).astype('int')
        context['hinano_expenses'] = (df['price'][(df.payer=='hinano') & (df.is_warikan==False)].sum()+(context['total_warikan_expenses'])/2).astype('int')

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

        # Expensesモデルをdfにする
        queryset = Expenses.objects.filter(date__year=year)
        queryset = queryset.filter(date__month=month)
        # クエリセットが何もない時はcontextを返す
        if not queryset:
            return context

        df = read_frame(queryset,
                        fieldnames=['date', 'payer', 'price', 'category' ,'is_warikan'])

        # グラフ作成クラスをインスタンス化
        gen = GraphGenerator()

        # 円グラフの素材を作成
        df_pie = pd.pivot_table(df, index='category', values='price', aggfunc=np.sum)
        pie_labels = list(df_pie.index.values)
        pie_values = [val[0] for val in df_pie.values]
        plot_pie = gen.month_pie(labels=pie_labels, values=pie_values)
        context['plot_pie'] = plot_pie

        # テーブルでのカテゴリと金額の表示用。
        # {カテゴリ:金額,カテゴリ:金額…}の辞書を作る
        context['table_set'] = df_pie.to_dict()['price']

        # totalの数字を計算して渡す
        context['total_expenses'] = df['price'].sum()

        context['yusuke_expenses'] = df['price'][(df.payer=='yusuke') & (df.is_warikan==False)].sum()

        # 日別の棒グラフの素材を渡す
        df_bar = pd.pivot_table(df, index='date', values='price', aggfunc=np.sum)
        dates = list(df_bar.index.values)
        heights = [val[0] for val in df_bar.values]
        plot_bar = gen.month_daily_bar(x_list=dates, y_list=heights)
        context['plot_bar'] = plot_bar

        return context

class TransitionView(TemplateView):
    template_name = 'transition.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expenses_queryset = Expenses.objects.all()

        expenses_df = read_frame(expenses_queryset,
                                fieldnames=['date', 'price'])
        # 日付カラムをdatetime化して、Y-m表記に変換
        expenses_df['date'] = pd.to_datetime(expenses_df['date'])
        expenses_df['month'] = expenses_df['date'].dt.strftime('%Y-%m')
        # 月ごとにpivot集計
        expenses_df = pd.pivot_table(expenses_df, index='month', values='price', aggfunc=np.sum)
        # x軸
        months = list(expenses_df.index.values)
        # y軸
        expenses = [y[0] for y in expenses_df.values]

        # グラフ生成
        gen = GraphGenerator()
        context['transition_plot'] = gen.transition_plot(x_list_expenses=months,
                                                   y_list_expenses=expenses)

        return context