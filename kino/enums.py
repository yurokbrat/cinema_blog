from django.db import models


class StatusChoose(models.TextChoices):
    waiting = "waiting", "Ожидание"
    processing = "processing", "В процессе"
    completed = "completed", "Выполнено"
    failed = "failed", "Произошла ошибка"


class QualityChoose(models.TextChoices):
    very_low = "360p", "360p"
    low = "480p", "480p"
    average = "720p", "720p"
    high = "1080p", "1080p"


class AgeChoose(models.TextChoices):
    zero = "zero", "0+"
    six = "six", "6+"
    twelve = "twelve", "12+"
    sixteen = "sixteen", "16+"
    eighteen = "eighteen", "18+"


class RateChoose(models.TextChoices):
    like = "like", "Лайк"
    dislike = "dislike", "Дизлайк"


class CrewChoose(models.TextChoices):
    director = "director", "Режиссёр"
    actor = "actor", "Актёр"
    cinematographer = "cinematographer", "Оператор (камера)"
    editor = "editor", "Монтажёр"
    screenwriter = "screenwriter","Сценарист"
    designer = "designer", "Художник-постановщик"
    sound_engineer = "sound_engineer", "Звукоинженер (звукорежиссёр)"
    composer = "composer", "Композитор"
    producer = "producer", "Продюсер"
