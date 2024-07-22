# Generated by Django 5.0.7 on 2024-07-20 23:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_share_album_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='share',
            name='review_score',
            field=models.DecimalField(decimal_places=1, default=None, max_digits=3, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)]),
        ),
    ]