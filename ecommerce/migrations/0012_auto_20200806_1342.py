# Generated by Django 3.0.7 on 2020-08-06 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0011_delete_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='imgurl',
        ),
        migrations.AddField(
            model_name='product',
            name='img_file',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]