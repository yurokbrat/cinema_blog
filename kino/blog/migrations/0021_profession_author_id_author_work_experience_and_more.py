# Generated by Django 4.2.10 on 2024-04-23 12:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0020_alter_author_user"),
    ]

    operations = [
        migrations.CreateModel(
            name="Profession",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Название")),
            ],
            options={
                "verbose_name": "профессия автора",
                "verbose_name_plural": "профессии авторов",
            },
        ),
        migrations.AddField(
            model_name="author",
            name="id",
            field=models.BigAutoField(
                auto_created=True,
                primary_key=True,
                serialize=False,
                verbose_name="ID",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="author",
            name="work_experience",
            field=models.CharField(blank=True, max_length=255, verbose_name="Стаж"),
        ),
        migrations.RemoveField(
            model_name="author",
            name="profession",
        ),
        migrations.AddField(
            model_name="author",
            name="profession",
            field=models.ManyToManyField(
                blank=True, to="blog.profession", verbose_name="Профессия"
            ),
        ),
    ]