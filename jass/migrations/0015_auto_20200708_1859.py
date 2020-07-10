# Generated by Django 3.0.5 on 2020-07-08 18:59

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('jass', '0014_auto_20200708_1827'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='seriesplayer',
            name='series',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player', to='jass.Series'),
        ),
    ]
