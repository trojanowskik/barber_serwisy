# Generated by Django 3.2.8 on 2022-01-22 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barber_serwis', '0003_auto_20220122_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
