# Generated by Django 3.0.5 on 2020-05-02 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jass', '0008_auto_20200501_1631'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='trumps',
            field=models.CharField(choices=[('spade', 'Spade'), ('heart', 'Heart'), ('diamond', 'Diamond'), ('club', 'Club')], default='klabberjass', max_length=7),
        ),
    ]