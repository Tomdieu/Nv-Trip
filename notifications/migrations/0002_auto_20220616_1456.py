# Generated by Django 3.2 on 2022-06-16 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='drivernotification',
            options={'ordering': ['-created']},
        ),
        migrations.AlterModelOptions(
            name='usernotification',
            options={'ordering': ['-created']},
        ),
    ]
