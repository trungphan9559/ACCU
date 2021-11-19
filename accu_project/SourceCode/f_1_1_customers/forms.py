from django import forms
from f_1_1_customers.models import *

class CustomerCreateForm(forms.ModelForm):
  class Meta:
    model = Customer
    fields = ['id', 'code', 'name','domain', 'site', 'customer_group','exclude_email','email_domain','is_prioritize','is_active']

  def clean_name(self):
    name = self.cleaned_data.get('name')
    customers = Customer.objects.filter(name=name)
    if len(customers) == 0:
      return name
    else:
      raise forms.ValidationError("Customer name is exist.")

  # def clean_domain(self):
  #   domain = self.cleaned_data.get('domain')
  #   customers = Customer.objects.filter(domain=domain)
  #   if len(customers) == 0:
  #     return domain
  #   else:
  #     raise forms.ValidationError("Customer domain is exist.")

