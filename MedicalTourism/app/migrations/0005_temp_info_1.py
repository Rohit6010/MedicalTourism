# Generated by Django 4.0.1 on 2022-11-30 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_temp_info_remove_disease_city_info_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Temp_info_1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(default='', max_length=100)),
                ('distance', models.CharField(default='', max_length=100)),
                ('time', models.CharField(default='', max_length=100)),
            ],
        ),
    ]
