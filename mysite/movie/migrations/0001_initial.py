# Generated by Django 3.1.2 on 2021-11-24 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('year', models.DateField()),
                ('poster', models.TextField()),
                ('description', models.TextField()),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('username', models.CharField(help_text='Enter field documentation', max_length=20)),
                ('password', models.CharField(help_text='Enter field documentation', max_length=20)),
            ],
            options={
                'ordering': ['user_id'],
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(verbose_name='rating')),
                ('timestamp', models.IntegerField(verbose_name='timestamp')),
                ('review', models.TextField(max_length=500, verbose_name='review')),
                ('movie_id', models.ForeignKey(db_column='movie_id', on_delete=django.db.models.deletion.PROTECT, to='movie.movie')),
                ('user_id', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.PROTECT, to='movie.user')),
            ],
            options={
                'ordering': ['user_id'],
            },
        ),
        migrations.CreateModel(
            name='BelongsToGenres',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.CharField(max_length=64)),
                ('movie_id', models.ForeignKey(db_column='movie_id', on_delete=django.db.models.deletion.PROTECT, to='movie.movie')),
            ],
            options={
                'ordering': ['genre'],
                'unique_together': {('movie_id', 'genre')},
            },
        ),
    ]