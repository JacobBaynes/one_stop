# Generated by Django 3.2.11 on 2022-01-13 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0015_auto_20220111_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='uuid',
            field=models.IntegerField(verbose_name='HPU ID'),
        ),
    ]
