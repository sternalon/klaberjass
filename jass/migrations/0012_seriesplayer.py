# Generated by Django 3.0.5 on 2020-07-07 20:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jass', '0011_playingcard_order_in_trick'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeriesPlayer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.SmallIntegerField()),
                ('series', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jass.Series')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]