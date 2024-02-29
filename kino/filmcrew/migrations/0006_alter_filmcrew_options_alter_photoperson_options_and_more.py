# Generated by Django 4.2.10 on 2024-02-24 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0007_alter_photofilm_options_alter_photoserial_options'),
        ('filmcrew', '0005_remove_filmcrew_birthplace_filmcrew_country'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='filmcrew',
            options={'verbose_name': 'Участник производства', 'verbose_name_plural': 'Участники производства'},
        ),
        migrations.AlterModelOptions(
            name='photoperson',
            options={'verbose_name': 'Фотография участника', 'verbose_name_plural': 'Фотографии участников'},
        ),
        migrations.AlterField(
            model_name='filmcrew',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cards.country', verbose_name='Место рождения'),
        ),
    ]