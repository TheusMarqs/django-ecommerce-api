# Generated by Django 5.1.2 on 2024-11-16 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default='image.png', upload_to=''),
            preserve_default=False,
        ),
    ]