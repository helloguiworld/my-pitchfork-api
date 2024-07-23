# Generated by Django 5.0.7 on 2024-07-23 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Search',
            fields=[
                ('q', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('albums', models.ManyToManyField(related_name='searches', to='spotify.album')),
            ],
        ),
    ]