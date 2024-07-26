# Generated by Django 5.0.7 on 2024-07-26 01:35

import django.core.validators
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_rename_share_shareclick'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shareclick',
            name='review_score',
            field=models.DecimalField(decimal_places=1, max_digits=3, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.0')), django.core.validators.MaxValueValidator(Decimal('10.0'))]),
        ),
    ]
