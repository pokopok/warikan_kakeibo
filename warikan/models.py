from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Categories(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return self.name

class Expenses(models.Model):
    date = models.DateField(default=timezone.now)
    payer = models.ForeignKey(
        Users, on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Categories, on_delete=models.CASCADE
    )
    price = models.IntegerField()
    memo = models.CharField(max_length=30, blank=True)
    is_warikan = models.BooleanField(default=False,help_text='割り勘対象ならTrue')

    class Meta:
        db_table = 'expenses'

    def __str__(self):
        return self.date