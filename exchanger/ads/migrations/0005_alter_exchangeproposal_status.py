# Generated by Django 5.2 on 2025-04-06 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0004_exchangeproposal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchangeproposal',
            name='status',
            field=models.CharField(auto_created='W', choices=[('W', 'Ожидает'), ('A', 'Принята')], max_length=1),
        ),
    ]
