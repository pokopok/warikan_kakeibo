from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone

from warikan.models import Categories, Expenses, Users

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='ユーザー名')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())

class ExpensesSearchForm(forms.Form):
    # 年の選択肢
    start_year = 2022
    end_year = timezone.now().year + 1
    years = [(year, f'{year}年') for year in reversed(range(start_year, end_year + 1))]
    years.insert(0, (0, ''))  # 空白の選択を追加
    YEAR_CHOICES = tuple(years)

    # 月の選択肢
    months = [(month, f'{month}月') for month in range(1, 13)]
    months.insert(0, (0, ''))
    MONTH_CHOICES = tuple(months)

    # 年の選択
    year = forms.ChoiceField(
        label='年での絞り込み',
        required=False,
        choices=YEAR_CHOICES,
        widget=forms.Select(attrs={'class': 'form'})
    )

    # 月の選択
    month = forms.ChoiceField(
        label='月での絞り込み',
        required=False,
        choices=MONTH_CHOICES,
        widget=forms.Select(attrs={'class': 'form'})
    )

    # キーワード
    key_word = forms.CharField(
        label='検索キーワード',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form',
                                      'autocomplete': 'off',
                                      'placeholder': 'メモ',
                                      })
    )

    # カテゴリー検索
    category = forms.ModelChoiceField(
        label='カテゴリでの絞り込み',
        required=False,
        queryset=Categories.objects.order_by('name'),
        widget=forms.Select(attrs={'class': 'form'})
    )

    # 支払者検索
    payer = forms.ModelChoiceField(
        label='支払者での絞り込み',
        required=False,
        queryset=Users.objects.order_by('user'),
        widget=forms.Select(attrs={'class': 'form'})
    )