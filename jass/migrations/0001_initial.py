# Generated by Django 3.0.5 on 2020-04-27 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('klabberjass', 'Klabberjass')], default='klabberjass', max_length=12)),
            ],
        ),
    ]
