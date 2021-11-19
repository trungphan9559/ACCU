from django.contrib import admin
from f_7_1_accounts.models import AccountUserSession
# Register your models here.

class AccountUserSessionAdmin(admin.ModelAdmin):
    list_display = ('user','last_updated','created_date')

admin.site.register(AccountUserSession,AccountUserSessionAdmin)
