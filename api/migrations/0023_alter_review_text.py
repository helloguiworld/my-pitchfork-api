# Generated by Django 5.0.7 on 2024-11-06 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_review_text_alter_review_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
    ]