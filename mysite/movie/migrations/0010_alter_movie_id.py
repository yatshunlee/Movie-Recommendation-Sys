# Generated by Django 3.2.9 on 2021-11-30 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0009_auto_20211130_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='id',
            field=models.IntegerField(max_length=64, primary_key=True, serialize=False),
        ),
    ]
