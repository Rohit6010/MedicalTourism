# Generated by Django 4.0.1 on 2022-11-14 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='id',
        ),
        migrations.AddField(
            model_name='patient',
            name='p_id',
            field=models.IntegerField(default=0, primary_key=True, serialize=False),
        ),
    ]
