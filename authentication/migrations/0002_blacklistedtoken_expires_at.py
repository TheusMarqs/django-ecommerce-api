# Generated by Django 4.2.3 on 2024-11-19 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blacklistedtoken',
            name='expires_at',
            field=models.DateTimeField(null=True),
        ),
    ]
