# Generated by Django 4.0.1 on 2022-11-14 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Disease',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('disease_name', models.CharField(max_length=100)),
                ('kg_id', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('phone', models.IntegerField()),
                ('state', models.CharField(max_length=500)),
                ('city', models.CharField(max_length=500)),
            ],
        ),
    ]
