import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("blog", "0018_alter_author_managers_remove_author_id_and_more"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="author",
            managers=[],
        ),
        migrations.RemoveField(
            model_name="author",
            name="user_ptr",
        ),
        migrations.AddField(
            model_name="author",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
    ]
