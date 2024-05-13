# Generated by Django 4.2.10 on 2024-05-10 11:26

import wagtail.blocks
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks
import wagtail.snippets.blocks
from django.db import migrations

import kino.blog.snippets


class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0027_alter_customimage_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='body',
            field=wagtail.fields.StreamField([('text', wagtail.blocks.RichTextBlock(
                features=['h2', 'h3', 'bold', 'italic', 'hr', 'ol', 'ul', 'blockquote'], label='Текст блога')), (
                                              'player', wagtail.embeds.blocks.EmbedBlock(
                                                  help_text='Вставьте ссылку из Youtube. Например: http://www.youtube.com/watch?v=Cd2ZTG43BJk',
                                                  label='URL-адрес', provider_name='YouTube')), ('image',
                                                                                                 wagtail.blocks.StructBlock(
                                                                                                     [('title',
                                                                                                       wagtail.blocks.CharBlock(
                                                                                                           label='Заголовок к блоку с изображениями',
                                                                                                           required=False)),
                                                                                                      ('image',
                                                                                                       wagtail.blocks.ListBlock(
                                                                                                           wagtail.images.blocks.ImageChooserBlock(
                                                                                                               label='Изображение'),
                                                                                                           label='Загрузите изображения'))],
                                                                                                     label='Изображения',
                                                                                                     required=False)), (
                                              'film', wagtail.blocks.StructBlock([('film',
                                                                                   wagtail.snippets.blocks.SnippetChooserBlock(
                                                                                       kino.blog.snippets.FilmBlog,
                                                                                       help_text='Укажите фильм',
                                                                                       label='Фильм')), ('film_fields',
                                                                                                         wagtail.blocks.MultipleChoiceBlock(
                                                                                                             choices=[(
                                                                                                                      'Название',
                                                                                                                      'Название'),
                                                                                                                      (
                                                                                                                      'Постер',
                                                                                                                      'Постер'),
                                                                                                                      (
                                                                                                                      'Страна',
                                                                                                                      'Страна'),
                                                                                                                      (
                                                                                                                      'Жанр',
                                                                                                                      'Жанр'),
                                                                                                                      (
                                                                                                                      'Описание',
                                                                                                                      'Описание'),
                                                                                                                      (
                                                                                                                      'Трейлер',
                                                                                                                      'Трейлер'),
                                                                                                                      (
                                                                                                                      'Кадры из карточки',
                                                                                                                      'Кадры из карточки')],
                                                                                                             help_text='Выберите поля, которые нужно добавить',
                                                                                                             label='Поля для заполнения'))],
                                                                                 help_text='Выберите фильм и настройте поля для отображения',
                                                                                 label='Фильм', required=False)), (
                                              'serial', wagtail.blocks.StructBlock([('serial',
                                                                                     wagtail.snippets.blocks.SnippetChooserBlock(
                                                                                         kino.blog.snippets.SerialBlog,
                                                                                         help_text='Укажите сериал',
                                                                                         label='Сериал')), (
                                                                                    'serial_fields',
                                                                                    wagtail.blocks.MultipleChoiceBlock(
                                                                                        choices=[
                                                                                            ('Название', 'Название'),
                                                                                            ('Постер', 'Постер'),
                                                                                            ('Страна', 'Страна'),
                                                                                            ('Жанр', 'Жанр'),
                                                                                            ('Описание', 'Описание'),
                                                                                            ('Трейлер', 'Трейлер'), (
                                                                                            'Кадры из карточки',
                                                                                            'Кадры из карточки')],
                                                                                        help_text='Выберите поля, которые нужно добавить',
                                                                                        label='Поля для заполнения'))],
                                                                                   help_text='Выберите сериал и настройте поля для отображения',
                                                                                   label='Сериал', required=False))],
                                             blank=True, verbose_name='Основная часть'),
        ),
    ]