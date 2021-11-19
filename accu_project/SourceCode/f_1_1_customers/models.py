from django.db import models
from django.urls import reverse
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from datetime import datetime
from dateutil.relativedelta import relativedelta

from f_1_2_sites.models import Site
# Create your models here.
class CustomerGroup(models.Model):
  name = models.CharField(max_length=50)
  site = models.ManyToManyField(Site, blank=True, verbose_name="契約サイト")

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('customer_group_list')
  
  class Meta:
    db_table = 'customer_group'

class Customer(models.Model):
  id = models.CharField(
    max_length=6,
    unique=True,
    primary_key=True
  )
  code = models.CharField(max_length=30, verbose_name="顧客コード")
  exclude_email = models.TextField(verbose_name="除外メールアドレス", help_text="例：@tpcompany.net")
  email_domain = models.TextField(verbose_name="除外ドメイン", help_text="例：tpcompany.net")
  name = models.CharField(max_length=30, verbose_name="顧客名")
  created_date = models.DateTimeField(auto_now_add=True, verbose_name="作成日")
  last_updated = models.DateTimeField(auto_now=True, verbose_name="更新日")
  domain = models.CharField(max_length=100,blank=True, verbose_name="サイトURL", help_text="例：https://www.tpcompany.net")
  customer_group = models.ForeignKey(CustomerGroup, on_delete=models.CASCADE, verbose_name="グループ")
  site = models.ManyToManyField(Site, blank=True, verbose_name="契約サイト")
  user = models.ManyToManyField(get_user_model(), blank=True, verbose_name="ユーザー")
  is_prioritize = models.BooleanField(default=False, verbose_name="プライオリタイズ")
  is_active = models.BooleanField(default=True, verbose_name="有効")

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('customer_list')


  class Meta:
    db_table = 'customer'

class CustomerContract(models.Model):
  goal_contacts_monthly = models.IntegerField(verbose_name="送信数ゴール（⽉）")
  goal_total_blogs = models.IntegerField(verbose_name="記事本数（⽉）")
  contract_period = models.IntegerField(verbose_name="契約期間 (ヶ月)")
  start_date = models.DateField(verbose_name="契約開始日")
  end_date = models.DateField(verbose_name="契約終了日")
  contract_period_option = models.IntegerField(verbose_name="オプション期間 (ヶ月)",null=True)
  start_date_option = models.DateField(verbose_name="オプション開始日",null=True)
  end_date_option = models.DateField(verbose_name="オプション終了日",null=True)
  created_date = models.DateTimeField(auto_now_add=True, verbose_name="作成日")
  last_updated = models.DateTimeField(auto_now=True, verbose_name="更新日")
  plan = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="plan", verbose_name="プラン")
  customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="顧客名")
  option = models.ManyToManyField(Group, db_table="customer_contract_option", related_name="option", blank=True, verbose_name="オプション")
  is_active = models.BooleanField(default=False, verbose_name="有効")
  is_priority = models.BooleanField(default=False, verbose_name="Priority")
  comment = models.TextField(verbose_name="Comment",blank=True)
  payment_method = models.CharField(
    choices=(
      ("once","Once"),
      ("monthly","Monthly"),
      ("completely free","Completely free"),
      ("other","Other"),
    ),
    default="monthly",
    max_length=20
  )
  goal_main_channel = models.IntegerField(default=0)
  goal_op1 = models.IntegerField(default=0)
  goal_op2 = models.IntegerField(default=0)
  site_id_main_channel = models.IntegerField(default=-1)
  site_id_op_1 = models.IntegerField(default=-1)
  site_id_op_2 = models.IntegerField(default=-1)
  is_free = models.BooleanField(default=False, verbose_name="無償")
  contract_period_free = models.IntegerField(verbose_name="無償期間",null=True)
  start_date_free = models.DateField(verbose_name="無償開始日",null=True)
  end_date_free = models.DateField(verbose_name="無償終了日",null=True)

  def __str__(self):
    return f'{self.customer.name} : {self.start_date}' 

  def get_absolute_url(self):
    return reverse('customer_contract_list')

  class Meta:
    db_table = 'customer_contract'

class CustomerSetting(models.Model):

  hb_form_id = models.TextField(verbose_name="HubspotフォームID")
  default_file_password = models.CharField(max_length=20, verbose_name="ファイルパスワード (デフォルト)")
  created_date = models.DateTimeField(auto_now_add=True, verbose_name="作成日")
  last_updated = models.DateTimeField(auto_now=True, verbose_name="更新日")
  customer = models.ForeignKey(Customer, on_delete= models.CASCADE, verbose_name="顧客名")
  site = models.ForeignKey(Site,on_delete = models.CASCADE, verbose_name="契約サイト")
  is_main_channel = models.BooleanField(null=True, default=False, verbose_name="主チャンネル")

  class Meta:
    db_table = 'customer_setting'

class CustomerSettingAudit(models.Model):
  field = models.CharField(max_length=20)
  record = models.ForeignKey(CustomerSetting, on_delete=models.CASCADE)
  old_value = models.CharField(max_length=100)
  new_value = models.CharField(max_length=100)
  user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
  create_date = models.DateTimeField(auto_now_add=True)

  class Meta:
    db_table = 'customer_setting_audit'

class CustomerGroupPlanOption(models.Model):
  customer_group = models.ForeignKey(CustomerGroup, on_delete=models.CASCADE)
  auth_group = models.ForeignKey(Group, on_delete=models.CASCADE)
  type = models.CharField(
    choices=(
      ("plan","Plan"),
      ("option","Option"),
    ),
    default="plan",
    max_length=20
  )
  sort = models.IntegerField()
  
  def __str__(self):
    return self.auth_group.name
  
  class Meta:
    db_table = 'customer_group_plan_option'

class CustomerSeminarSetting(models.Model):
  name = models.CharField(max_length=255,null=True)
  list_hb_id = models.IntegerField(null=True)
  lp_id = models.CharField(max_length=45,null=True)
  dict_properties = models.TextField(null=True)
  last_updated = models.DateTimeField(auto_now=True)
  created_date = models.DateTimeField(auto_now_add=True)
  site = models.ForeignKey(Site,on_delete = models.CASCADE)
  customer = models.ForeignKey(Customer,on_delete = models.CASCADE)
  file_password = models.CharField(max_length=20,null=True)
  
  class Meta:
    db_table = 'customer_seminar_setting'



