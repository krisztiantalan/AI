# Generated by Django 4.2.1 on 2023-05-11 13:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='asset',
            old_name='bar_code',
            new_name='barcode',
        ),
    ]
