# Generated by Django 4.1 on 2022-09-16 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='likes_count',
            field=models.IntegerField(default=0),
        ),
    ]
