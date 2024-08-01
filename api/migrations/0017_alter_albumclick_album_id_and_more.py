# Generated by Django 5.0.7 on 2024-07-31 03:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_alter_review_album'),
    ]

    operations = [
        migrations.AlterField(
            model_name='albumclick',
            name='album_id',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='trackscore',
            name='track',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='scores', to='api.review'),
        ),
    ]