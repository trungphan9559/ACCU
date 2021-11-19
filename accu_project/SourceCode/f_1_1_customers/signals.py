from django.db.models.signals import post_save, pre_delete, m2m_changed
from django.dispatch import receiver
from .models import CustomerContract, Customer
from django.contrib.auth.models import Group
#==================================
#====== Customer Contract =========
#==================================
@receiver(m2m_changed, sender=CustomerContract.option.through)
def m2m_changed_customer_contract(sender, instance, action, **kwargs):
  for user in instance.customer.user.all():
    for pk in kwargs['pk_set']:
      if action == 'post_add':
        user.groups.add(Group.objects.get(pk=pk))
      elif action == 'post_remove':
        user.groups.remove(Group.objects.get(pk=pk))

@receiver(post_save, sender=CustomerContract)
def post_save_create_or_update_contract(sender, instance, **kwargs):
  if instance.is_active:
    #1)Set tất cả các hợp đồng khác về inactive
    # CustomerContract.objects.filter(customer=instance.customer).exclude(pk=instance.pk).update(is_active = 0)

    #2)Phân quyền
    for user in instance.customer.user.all():
      user.groups.clear()
      user.groups.add(instance.plan)
      for option in instance.option.all():
        user.groups.add(option)

@receiver(pre_delete, sender=CustomerContract)
def pre_delete_customer_contract(sender, instance, **kwargs):
  if instance.is_active:
    for user in instance.customer.user.all():
      user.groups.clear()