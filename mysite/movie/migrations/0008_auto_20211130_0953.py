# Generated by Django 3.1.2 on 2021-11-30 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0007_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
