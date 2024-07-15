# Generated by Django 5.0.7 on 2024-07-15 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Share',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('album_id', models.CharField(max_length=50)),
                ('type', models.CharField(choices=[('square', 'Square'), ('stories', 'Stories')], max_length=10)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
