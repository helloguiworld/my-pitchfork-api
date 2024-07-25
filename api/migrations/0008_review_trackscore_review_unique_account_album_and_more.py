# Generated by Django 5.0.7 on 2024-07-25 04:31

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_albumclick'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('album', models.CharField(max_length=50)),
                ('score', models.DecimalField(decimal_places=1, max_digits=3, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.account')),
            ],
        ),
        migrations.CreateModel(
            name='TrackScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('track', models.CharField(max_length=50)),
                ('score', models.DecimalField(decimal_places=1, max_digits=3, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.account')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.review')),
            ],
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('account', 'album'), name='unique_account_album'),
        ),
        migrations.AddConstraint(
            model_name='trackscore',
            constraint=models.UniqueConstraint(fields=('account', 'track'), name='unique_account_track'),
        ),
    ]
