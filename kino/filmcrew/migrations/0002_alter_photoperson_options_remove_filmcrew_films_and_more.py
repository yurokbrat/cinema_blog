# Generated by Django 4.2.10 on 2024-02-22 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filmcrew', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='photoperson',
            options={'verbose_name': 'Фото'},
        ),
        migrations.RemoveField(
            model_name='filmcrew',
            name='films',
        ),
        migrations.RemoveField(
            model_name='filmcrew',
            name='serials',
        ),
        migrations.AlterField(
            model_name='filmcrew',
            name='birthday',
            field=models.DateField(verbose_name='Дата рождения'),
        ),
    ]