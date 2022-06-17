# Generated by Django 3.2.5 on 2022-06-08 05:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='car_type',
            field=models.CharField(choices=[('CAR', 'CAR'), ('BUS', 'BUS')], max_length=20, verbose_name='Vehicle Type'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]