# Generated by Django 3.2.8 on 2021-10-28 18:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('query_prototype', '0002_auto_20211028_1758'),
    ]

    operations = [
        migrations.RenameField(
            model_name='queryfieldsmodel',
            old_name='isControl',
            new_name='is_control',
        ),
    ]