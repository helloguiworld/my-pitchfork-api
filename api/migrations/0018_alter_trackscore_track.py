# Generated by Django 5.0.7 on 2024-07-31 07:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_alter_albumclick_album_id_and_more'),
        ('spotify', '0004_remove_album_name_alter_album_id_alter_search_q_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trackscore',
            name='track',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='scores', to='spotify.track'),
        ),
    ]
