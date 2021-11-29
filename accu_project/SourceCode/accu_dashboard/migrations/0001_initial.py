# Generated by Django 3.2.9 on 2021-11-29 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='R_ALARM_LOG',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('district', models.CharField(max_length=255)),
                ('provice', models.CharField(max_length=255)),
                ('groups', models.CharField(max_length=255)),
                ('network', models.CharField(max_length=255)),
                ('vendor', models.CharField(max_length=255)),
                ('ne', models.CharField(max_length=255)),
                ('site', models.CharField(max_length=255)),
                ('sdate', models.DateTimeField(null=True, verbose_name='')),
                ('edate', models.DateTimeField(null=True, verbose_name='')),
                ('alarm_type', models.CharField(max_length=255)),
                ('alarm_name', models.CharField(max_length=255)),
                ('alarm_info', models.CharField(max_length=2555)),
            ],
        ),
    ]