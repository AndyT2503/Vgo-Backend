# Generated by Django 3.0.5 on 2020-06-26 12:10

from django.db import migrations, models
import vgo.apps.post.models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0013_auto_20200626_1905'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=vgo.apps.post.models.upload_location),
        ),
        migrations.DeleteModel(
            name='Images',
        ),
    ]
