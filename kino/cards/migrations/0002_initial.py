# Generated by Django 4.2.10 on 2024-02-22 11:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cards', '0001_initial'),
        ('filmcrew', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='serial',
            name='film_crew',
            field=models.ManyToManyField(to='filmcrew.filmcrew', verbose_name='Съемочная группа'),
        ),
        migrations.AddField(
            model_name='serial',
            name='genre',
            field=models.ManyToManyField(to='cards.genre', verbose_name='Жанр'),
        ),
        migrations.AddField(
            model_name='photoserial',
            name='serial',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cards.serial', verbose_name='Карточка'),
        ),
        migrations.AddField(
            model_name='photofilm',
            name='film',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cards.film', verbose_name='Карточка'),
        ),
        migrations.AddField(
            model_name='film',
            name='country',
            field=models.ManyToManyField(to='cards.country', verbose_name='Страна производитель'),
        ),
        migrations.AddField(
            model_name='film',
            name='film_crew',
            field=models.ManyToManyField(to='filmcrew.filmcrew', verbose_name='Съемочная группа'),
        ),
        migrations.AddField(
            model_name='film',
            name='genre',
            field=models.ManyToManyField(to='cards.genre', verbose_name='Жанр'),
        ),
    ]