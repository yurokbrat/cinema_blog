# Generated by Django 4.1.8 on 2024-04-18 12:59

import modelcluster.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0011_remove_blogpage_film_blogpage_films"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="blogpage",
            name="films",
        ),
        migrations.AddField(
            model_name="blogpage",
            name="film",
            field=modelcluster.fields.ParentalManyToManyField(
                blank=True, to="blog.film"
            ),
        ),
    ]
