# Generated by Django 3.2.9 on 2021-11-23 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0003_alter_person_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='class_level',
            field=models.CharField(max_length=40, null=True),
        ),
    ]
