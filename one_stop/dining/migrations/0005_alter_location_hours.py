# Generated by Django 3.2.11 on 2022-01-13 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dining', '0004_alter_location_hours'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='hours',
            field=models.TextField(),
        ),
    ]
