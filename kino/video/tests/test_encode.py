from pathlib import Path

import pytest
from django.conf import settings

from kino.enums import StatusChoose
from kino.utils.stages_of_video.check_urls_to_quality import urls_to_quality
from kino.utils.stages_of_video.encoding import load_video
from kino.utils.stages_of_video.record import record_video
from kino.video.models import Task, VideoQuality
from kino.video.tests.utils.base_video import BaseVideoCard
from kino.video.tests.utils.check_quality_video import check_quality_video
from kino.video.tests.utils.convert import coding_video


@pytest.mark.skip(reason="You only need to test video encoding locally")
class TestEncodeVideo(BaseVideoCard):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.task = Task.objects.create(
            media=cls.media,
            status=StatusChoose.processing,
        )
        coding_video(cls.media, cls.task, cls.quality, cls.aspect_ratio)
        cls.output_file = Path(
            settings.PATH_TO_MEDIA,
            "tests",
            cls.media.card.name,
            f"{cls.quality}.mp4",
        )

    # Тесты конвертации видео
    def test_create_output_video(self):
        self.assertTrue(
            self.output_file.exists(),
            f"Файл не был создан по адресу {self.output_file}",
        )

    def test_width_output_video(self):
        width, height = check_quality_video(self.output_file)
        self.assertEqual(
            width,
            self.quality * self.aspect_ratio,
            f"Сконвертированное видео создано размером {width}x{height}",
        )

    def test_height_output_video(self):
        width, height = check_quality_video(self.output_file)
        self.assertEqual(
            height,
            self.quality,
            f"Сконвертированное видео создано размером {width}x{height}",
        )

    def test_failed_task_status_with_missing_file(self):
        self.media.source_link = f"{settings.PATH_TO_MEDIA}/source/films/missing_file.mp4"
        task = Task.objects.get(media=self.media)
        record_video(self.media.source_link, self.media.id, task.id)
        task.refresh_from_db()
        self.assertEqual(
            task.status,
            StatusChoose.failed,
            f"Задача выполнения кодировки: {task}",
        )

    def test_failed_task_status_with_incorrect_format(self):
        self.media.source_link = f"{settings.PATH_TO_MEDIA}/incorrect_files/image.jpg"
        task = Task.objects.get(media=self.media)
        record_video(self.media.source_link, self.media.id, task.id)
        task.refresh_from_db()
        self.assertEqual(
            task.status,
            StatusChoose.failed,
            f"Задача выполнения кодировки: {task}",
        )

    # Тесты статусов задач
    @pytest.mark.run(order=1)
    def test_processing_task_status(self):
        self.assertEqual(
            self.task.status,
            StatusChoose.processing,
            f"Запись о статусе конвертации: {self.task}",
        )

    @pytest.mark.run(order=2)
    def test_completed_task_status(self):
        load_video(self.output_file, self.media.id, self.task.id)
        self.task.refresh_from_db()
        self.assertEqual(
            self.task.status,
            StatusChoose.completed,
            f"Запись о статусе конвертации: {self.task}",
        )

    # Тест на добавление ссылки на видео
    @pytest.mark.run(order=3)
    def test_add_video_url(self):
        urls_to_quality(self.media, self.quality, self.output_file)
        url_to_video = VideoQuality.objects.get(
            media=self.media,
            quality=self.quality,
            video_url=self.output_file,
        )
        self.assertTrue(
            url_to_video,
            f"Запись о ссылке на видео: {url_to_video}",
        )
