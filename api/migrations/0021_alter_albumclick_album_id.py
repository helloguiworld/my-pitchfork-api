# Generated by Django 5.0.7 on 2024-07-31 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_alter_albumclick_album_id_alter_searchclick_q_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='albumclick',
            name='album_id',
            field=models.CharField(max_length=255),
        ),
    ]