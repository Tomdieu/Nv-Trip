# Generated by Django 3.2 on 2022-06-10 09:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_drive'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='drive',
            options={'ordering': ['created'], 'verbose_name': 'drive', 'verbose_name_plural': 'drives'},
        ),
        migrations.AddField(
            model_name='drive',
            name='date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vehicle',
            name='status',
            field=models.CharField(choices=[('online', 'online'), ('offline', 'offline')], default='offline', max_length=10, verbose_name='status'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
