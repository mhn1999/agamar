# Generated by Django 3.2.8 on 2021-12-17 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='reply',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='chat.message'),
        ),
        migrations.AlterField(
            model_name='message',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]