from f_1_1_customers.models import Customer, CustomerContract
from django.contrib.auth import get_user_model
from datetime import datetime

def add_user_to_customer(customer_id, user_id):
  #1)Thông tin của customer
  customer = Customer.objects.get(pk=customer_id)
  # customer_contract = CustomerContract.objects.filter(customer=customer, is_active=True)
  customer_contract = CustomerContract.objects.filter(customer = customer, start_date__lte = datetime.now().date(), end_date__gte = datetime.now().date())

  if not customer_contract:
      return
  else:
      customer_contract = customer_contract[0]

  #2)Phân quyền user
  user = get_user_model().objects.get(pk=user_id)
  #2.1)Xóa quyền
  user.groups.clear()

  #2.2)Thêm quyền
  user.groups.add(customer_contract.plan)
  for option in customer_contract.option.all():
    user.groups.add(option)