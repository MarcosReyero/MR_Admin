# Generated by Django 4.2.13 on 2024-06-09 20:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('miapp', '0002_post_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
    ]
