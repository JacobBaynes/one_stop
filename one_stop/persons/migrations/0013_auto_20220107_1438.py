# Generated by Django 3.2.9 on 2022-01-07 19:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('persons', '0012_alter_person_mname'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={'ordering': ['uuid']},
        ),
        migrations.AlterField(
            model_name='person',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
