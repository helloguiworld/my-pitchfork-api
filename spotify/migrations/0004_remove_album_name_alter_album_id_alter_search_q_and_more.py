# Generated by Django 5.0.7 on 2024-07-31 03:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify', '0003_alter_search_q'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='name',
        ),
        migrations.AlterField(
            model_name='album',
            name='id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='search',
            name='q',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, unique=True),
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('data', models.JSONField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tracks', to='spotify.album')),
            ],
        ),
    ]
