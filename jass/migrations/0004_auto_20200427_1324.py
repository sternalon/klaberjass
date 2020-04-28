# Generated by Django 3.0.5 on 2020-04-27 11:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('jass', '0003_playingcard'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='game',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]