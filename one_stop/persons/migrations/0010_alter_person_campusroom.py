# Generated by Django 3.2.9 on 2022-01-04 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0009_alter_person_mname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='campusroom',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Campus Room'),
        ),
    ]
