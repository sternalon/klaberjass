# Generated by Django 3.0.5 on 2020-05-01 14:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jass', '0007_series'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='series',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='jass.Series'),
        ),
        migrations.AlterField(
            model_name='series',
            name='score1',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='series',
            name='score2',
            field=models.IntegerField(default=0),
        ),
    ]