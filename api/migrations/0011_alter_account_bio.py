# Generated by Django 5.0.7 on 2024-07-27 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_shareclick_review_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='bio',
            field=models.TextField(blank=True, default='', max_length=500),
        ),
    ]