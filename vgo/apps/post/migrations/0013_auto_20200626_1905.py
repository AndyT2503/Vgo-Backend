# Generated by Django 3.0.5 on 2020-06-26 12:05

from django.db import migrations, models
import django.db.models.deletion
import vgo.apps.post.models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0010_auto_20200626_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='image',
            field=models.ImageField(upload_to=vgo.apps.post.models.upload_location),
        ),
        migrations.AlterField(
            model_name='images',
            name='post',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='post.Post'),
        ),
    ]
