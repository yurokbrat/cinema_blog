# Generated by Django 4.1.8 on 2024-04-18 12:48

import django.db.models.deletion
import modelcluster.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailimages", "0025_alter_image_file_alter_rendition_file"),
        ("blog", "0009_country_genre_remove_film_tags_alter_blogpage_tags_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="blogpage",
            options={"verbose_name": "страница", "verbose_name_plural": "страницы"},
        ),
        migrations.AlterField(
            model_name="blogpage",
            name="date",
            field=models.DateField(verbose_name="Дата публикации"),
        ),
        migrations.AlterField(
            model_name="blogpage",
            name="film",
            field=modelcluster.fields.ParentalManyToManyField(
                blank=True, to="blog.film"
            ),
        ),
        migrations.AlterField(
            model_name="blogpagegalleryimage",
            name="image",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="wagtailimages.image",
                verbose_name="Фотография",
            ),
        ),
        migrations.AlterField(
            model_name="blogpagegalleryimage",
            name="page",
            field=modelcluster.fields.ParentalKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="gallery_images",
                to="blog.blogpage",
                verbose_name="Блог",
            ),
        ),
        migrations.AlterField(
            model_name="film",
            name="name",
            field=models.CharField(max_length=255, verbose_name="Название фильма"),
        ),
        migrations.AlterField(
            model_name="film",
            name="year",
            field=models.PositiveSmallIntegerField(
                blank=True, null=True, verbose_name="Год выхода"
            ),
        ),
    ]
