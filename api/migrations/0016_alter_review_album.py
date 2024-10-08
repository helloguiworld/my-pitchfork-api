# Generated by Django 5.0.7 on 2024-07-31 01:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_alter_trackscore_review'),
        ('spotify', '0003_alter_search_q'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='album',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reviews', to='spotify.album'),
        ),
    ]
