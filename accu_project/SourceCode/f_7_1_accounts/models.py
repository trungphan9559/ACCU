from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
# Create your models here

class AccountUserSession(models.Model):
  secret_key = models.CharField(max_length=255)
  last_token = models.CharField(max_length=10,default='')
  sent_times = models.IntegerField(default=0)
  last_updated = models.DateTimeField(auto_now=True)
  created_date = models.DateTimeField(auto_now_add=True)
  is_verified = models.BooleanField(default=0)
  last_verify_token = models.CharField(max_length=255,default='')
  user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)

  class Meta:
    db_table = 'account_user_session'