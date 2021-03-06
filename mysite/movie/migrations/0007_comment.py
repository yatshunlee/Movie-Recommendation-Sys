# Generated by Django 3.1.2 on 2021-11-30 01:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movie', '0006_auto_20211126_2134'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('comment', models.TextField(max_length=500)),
                ('timestamp', models.IntegerField()),
                ('rating_id', models.ForeignKey(db_column='rating_id', on_delete=django.db.models.deletion.PROTECT, to='movie.rating')),
                ('user_id', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
