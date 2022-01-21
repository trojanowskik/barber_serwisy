# Generated by Django 4.0.1 on 2022-01-21 17:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('barber_serwis', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skills',
            name='skills_name',
            field=models.CharField(default='', max_length=50, unique=True),
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(default='', max_length=255)),
                ('date', models.DateTimeField()),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='barber_serwis.client')),
                ('skills', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='barber_serwis.skills')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
    ]
