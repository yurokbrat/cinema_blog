# Generated by Django 4.2.10 on 2024-02-22 11:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilmCrew',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
                ('profession', models.CharField(max_length=155, verbose_name='Профессия')),
                ('birthday', models.DateTimeField(verbose_name='Дата рождения')),
                ('birthplace', models.CharField(max_length=155, verbose_name='Место рождения')),
                ('films', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cards.film', verbose_name='Фильмы')),
                ('serials', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cards.serial', verbose_name='Сериалы')),
            ],
        ),
        migrations.CreateModel(
            name='PhotoPerson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo_person', models.ImageField(upload_to='photos_persons/', verbose_name='Фото')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='filmcrew.filmcrew')),
            ],
        ),
    ]