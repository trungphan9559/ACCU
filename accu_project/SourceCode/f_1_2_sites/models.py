import random
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.models import Group

# Create your models here.

TYPE_CHOICES = (
  ("coporate","Coporate"),
  ("channel","Channel"),
)
class Site(models.Model):
  id = models.CharField(
    max_length=6,
    unique=True,
    primary_key=True
  )
  name = models.CharField(max_length=30)
  url = models.CharField(max_length=50)
  logo = models.CharField(max_length=200,blank=True)
  created_date = models.DateTimeField(auto_now_add=True)
  last_updated = models.DateTimeField(auto_now=True)
  contract_start_date = models.DateField(auto_now=True)
  is_active = models.BooleanField(default=True)
  type = models.CharField(
    max_length=20,
    choices=TYPE_CHOICES,
    default="coporate"
  )
  en_name = models.CharField(max_length=255,blank=True)
  asana_project_id = models.CharField(max_length=50,blank=True)
  person_in_charge = models.ForeignKey(get_user_model(), on_delete= models.SET_NULL,related_name="person_in_charge", null=True)
  person_in_charge_management = models.ForeignKey(get_user_model(), on_delete= models.SET_NULL,related_name="person_in_charge_management", null=True)
  
  def __str__(self):
    url = self.url
    url = url.replace('https://www.','')
    url = url.replace('http://www.','')
    return f"{self.name} ({url})"
  
  def get_absolute_url(self):
    return reverse('site_list')
  class Meta:
    db_table = 'site'

class SiteAuth(models.Model):
  last_ga_refresh_token = models.CharField(max_length=200,default='-1')
  ga_account_id = models.CharField(max_length=30,default='-1')
  ga_view_id = models.CharField(max_length=30,default='-1')
  ga_property_id = models.CharField(max_length=30,default='-1')
  last_gsc_refresh_token = models.CharField(max_length=200,default='-1')
  gsc_site_url = models.CharField(max_length=200,default='-1')
  last_hub_access_token = models.CharField(max_length=200,default='-1')
  last_hub_refresh_token = models.CharField(max_length=200,default='-1')
  hub_id = models.CharField(max_length = 30,default='-1')
  hub_view_id = models.CharField(max_length = 30,default='-1')
  site = models.ForeignKey(Site, on_delete=models.CASCADE)
  created_date = models.DateTimeField(auto_now_add=True)
  last_updated = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = 'site_auth'

class SitePropertySetting(models.Model):
  site = models.ForeignKey(Site, on_delete=models.CASCADE)
  property_label = models.CharField(max_length=255,null=True)
  property_internal_name = models.CharField(max_length=255,null=True)
  properties = models.TextField(null=True)
  type = models.CharField(max_length=20,null=True)
  sort = models.IntegerField(null=True)

  class Meta:
    db_table = 'site_property_setting'

class SiteGroupPageSetting(models.Model):
  group_name = models.CharField(max_length=255,null=True)
  landing_page_master_id = models.CharField(max_length=255,null=True,default="")
  thanks_page_master_id = models.CharField(max_length=255,null=True,default="")
  resource_top_page_id = models.CharField(max_length=255,null=True,default="")
  hb_list_master_id = models.CharField(max_length=255,null=True,default="")
  hb_list_name_default = models.CharField(max_length=255,null=True,default="")
  folder_pdf_id = models.CharField(max_length=255,null=True,default="")
  folder_thumb_id = models.CharField(max_length=255,null=True,default="")
  folder_cta_id = models.CharField(max_length=255,null=True,default="")
  cta_middle_template_file = models.CharField(max_length=255,null=True,default="")
  cta_footer_template_file = models.CharField(max_length=255,null=True,default="")
  cta_footer_mobile_setting = models.TextField(default="{}")
  is_common = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  site = models.ForeignKey(Site, on_delete=models.CASCADE)
  created_date = models.DateTimeField(auto_now_add=True)
  last_updated = models.DateTimeField(auto_now=True)
  
  class Meta:
    db_table = 'site_group_page_setting'

class SiteGroupCTASetting(models.Model):
  group_cta_name = models.CharField(max_length=255,null=True)
  folder_cta_id = models.CharField(max_length=255,null=True,default="")
  cta_footer_setting = models.TextField(default="{}")
  cta_middle_setting = models.TextField(default="{}")
  cta_mobile_setting = models.TextField(default="{}")
  cta_sidebar_setting = models.TextField(default="{}")
  is_active = models.BooleanField(default=True)
  site = models.ForeignKey(Site, on_delete=models.CASCADE)
  created_date = models.DateTimeField(auto_now_add=True)
  last_updated = models.DateTimeField(auto_now=True)
  class Meta:
    db_table = 'site_group_cta_setting'