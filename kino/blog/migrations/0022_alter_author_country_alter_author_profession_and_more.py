# Generated by Django 4.2.10 on 2024-04-23 13:13

import django.db.models.deletion
import modelcluster.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("cards", "0025_alter_film_film_crew_alter_serial_film_crew"),
        ("blog", "0021_profession_author_id_author_work_experience_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="author",
            name="country",
            field=models.OneToOneField(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="country",
                to="cards.country",
                verbose_name="Страна",
            ),
        ),
        migrations.AlterField(
            model_name="author",
            name="profession",
            field=modelcluster.fields.ParentalManyToManyField(
                blank=True, to="blog.profession", verbose_name="Профессия"
            ),
        ),
        migrations.AlterField(
            model_name="author",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
        migrations.AlterField(
            model_name="author",
            name="work_experience",
            field=models.PositiveSmallIntegerField(
                blank=True, max_length=255, verbose_name="Стаж"
            ),
        ),
    ]