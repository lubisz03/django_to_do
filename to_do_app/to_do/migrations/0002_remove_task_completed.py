# Generated by Django 4.2.7 on 2023-11-29 19:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('to_do', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='completed',
        ),
    ]
