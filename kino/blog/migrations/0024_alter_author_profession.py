# Generated by Django 4.2.10 on 2024-04-24 11:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0023_alter_author_work_experience"),
    ]

    operations = [
        migrations.AlterField(
            model_name="author",
            name="profession",
            field=models.ManyToManyField(
                blank=True, to="blog.profession", verbose_name="Профессия"
            ),
        ),
    ]
