# Generated by Django 3.2.8 on 2021-12-13 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookmanage', '0011_books_category'),
        ('authentication', '0012_alter_customuser_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='books_ordered',
            field=models.ManyToManyField(related_name='books_ordered', to='bookmanage.books'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='favourite',
            field=models.ManyToManyField(related_name='favourote', to='bookmanage.books'),
        ),
    ]