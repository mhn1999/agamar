# Generated by Django 3.2.8 on 2021-10-24 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.IntegerField(null=True, unique=True),
        ),
    ]