# Generated by Django 5.0.7 on 2024-07-23 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify', '0002_search'),
    ]

    operations = [
        migrations.AlterField(
            model_name='search',
            name='q',
            field=models.CharField(max_length=50, primary_key=True, serialize=False, unique=True),
        ),
    ]
