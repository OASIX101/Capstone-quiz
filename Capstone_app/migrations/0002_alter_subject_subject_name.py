# Generated by Django 4.1.2 on 2022-11-11 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Capstone_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='subject_name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
