# Generated by Django 3.2.9 on 2021-11-24 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='year',
            field=models.CharField(max_length=5),
        ),
    ]
