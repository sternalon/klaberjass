# Generated by Django 3.0.5 on 2020-07-08 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jass', '0013_auto_20200707_2044'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='name',
            new_name='game_type',
        ),
        migrations.AddField(
            model_name='series',
            name='game_type',
            field=models.CharField(choices=[('klabberjass', 'Klabberjass')], default='klabberjass', max_length=12),
        ),
    ]
