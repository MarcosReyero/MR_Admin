# Generated by Django 5.1 on 2024-10-11 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miapp', '0007_alter_perfilusuario_foto_perfil'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='post_images/'),
        ),
    ]
