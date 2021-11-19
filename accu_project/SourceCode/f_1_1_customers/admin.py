import random
from django.contrib import admin
from f_1_1_customers.models import *
# Register your models here.

admin.site.register(CustomerGroup)
admin.site.register(Customer)
admin.site.register(CustomerContract)
admin.site.register(CustomerSetting)
admin.site.register(CustomerSettingAudit)
admin.site.register(CustomerGroupPlanOption)
admin.site.register(CustomerSeminarSetting)
