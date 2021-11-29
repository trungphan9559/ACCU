from django.db import models

# Create your models here.
class R_ALARM_LOG(models.Model):
  district = models.CharField(max_length=255)
  provice = models.CharField(max_length=255)
  groups = models.CharField(max_length=255)
  network = models.CharField(max_length=255)
  vendor = models.CharField(max_length=255)
  ne = models.CharField(max_length=255)
  site = models.CharField(max_length=255)
  sdate = models.DateTimeField(null=True, verbose_name="")
  edate = models.DateTimeField(null=True, verbose_name="")

  alarm_type = models.CharField(max_length=255)
  alarm_name = models.CharField(max_length=255)
  alarm_info = models.CharField(max_length=2555)


