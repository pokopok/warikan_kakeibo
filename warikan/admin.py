from django.contrib import admin
from warikan.models import Users, Categories, Expenses
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class CategoriesResource(resources.ModelResource):
    class Meta:
        model = Categories

class CategoriesAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name']
    resource_class = CategoriesResource

class ExpensesResource(resources.ModelResource):
    class Meta:
        model = Expenses

class ExpensesAdmin(ImportExportModelAdmin):
    search_fields = ('memo',)
    list_display = ['date', 'payer', 'category', 'is_warikan', 'price', 'memo']
    list_filter = ('category',)
    ordering = ('-date',)

    resource_class = ExpensesResource

admin.site.register(Users)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Expenses, ExpensesAdmin)