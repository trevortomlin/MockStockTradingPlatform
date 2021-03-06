# Generated by Django 3.2.9 on 2021-11-28 16:23

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0004_auto_20211128_0812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='transactionDate',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 28, 8, 23, 1, 837174), verbose_name='transaction date'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL),
        ),
    ]
