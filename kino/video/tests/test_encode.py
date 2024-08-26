from pathlib import Path

import pytest
from django.conf import settings

from kino.enums import StatusChoose
from kino.utils.stages_of_video.check_urls_to_quality import urls_to_quality
from kino.utils.stages_of_video.encoding import load_video
from kino.utils.stages_of_video.record import record_video
from kino.video.models import Task, VideoQuality, Media
from kino.video.tests.utils.base_video import BaseVideoCard
from kino.video.tests.utils.check_quality_video import check_quality_video
from kino.video.tests.utils.convert import coding_video


class TestEncodeVideo(BaseVideoCard):
    task: Task
    output_file: Path
    media: Media

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.task = Task.objects.create(
            media=cls.media,
            status=StatusChoose.processing,
        )
        coding_video(cls.media, cls.task, cls.quality, cls.aspect_ratio)
        card_name: str | None = getattr(cls.media.card, "name", None)
        if card_name:
            cls.output_file = Path(
                settings.PATH_TO_MEDIA,
                "tests",
                card_name,
                f"{cls.quality}.mp4",
            )

    # Тесты конвертации видео
    def test_create_output_video(self):
        self.assertTrue(
            self.output_file.exists(),
            f"Файл не был создан по адресу {self.output_file}",
        )

    def test_resolution_output_video(self):
        if result := check_quality_video(self.output_file):
            width, height = result
            self.assertEqual(
                width,
                self.quality * self.aspect_ratio,
                f"Сконвертированное видео создано размером {width}x{height}",
            )
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

    @pytest.mark.skipif(
        settings.AWS_ACCESS_KEY_ID != "" and settings.AWS_SECRET_ACCESS_KEY != "",
        reason="AWS credentials are set, skipping test",
    )
    def test_completed_task_status(self):
        load_video(self.output_file, self.media.id, self.task.id)
        self.task.refresh_from_db()
        self.assertEqual(
            self.task.status,
            StatusChoose.completed,
            f"Запись о статусе конвертации: {self.task}",
        )

    # Тест на добавление ссылки на видео
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
