# Generated by Django 4.0.1 on 2022-02-16 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dining', '0005_alter_location_hours'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='phone_number',
            field=models.CharField(max_length=16, null=True),
        ),
    ]
