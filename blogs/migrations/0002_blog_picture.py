# Generated by Django 4.1.4 on 2022-12-29 05:37

import blogs.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blogs", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="blog",
            name="picture",
            field=models.ImageField(blank=True, upload_to=blogs.models.Blog.nameFile),
        ),
    ]