# Generated by Django 3.2.9 on 2021-11-23 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0005_alter_person_dob'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='phone',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]
