# Generated by Django 5.1.6 on 2025-02-26 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('borrowing', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='borrowing',
            options={'ordering': ['-borrow_date']},
        ),
    ]
