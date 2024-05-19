from pathlib import Path
from unittest.mock import patch

import pytest
from django.conf import settings

from config.settings.base import env
from kino.enums import StatusChoose
from kino.video.models import Task, Media
from kino.video.tasks import download_video
from kino.video.tests.utils.base_video import BaseVideoCard
from kino.video.tests.utils.convert import coding_video


@pytest.mark.django_db()
class TestVideoTasks(BaseVideoCard):
    output_file: Path
    media: Media

    @patch("kino.video.tasks.encode_video.delay")
    def test_create_task(self, mock_encode_video):
        download_video(self.media.id)
        task = Task.objects.filter(media=self.media).first()
        self.assertIsNotNone(task)

    @patch("kino.video.tasks.encode_video.delay")
    @pytest.mark.skipif(
        env("AWS_ACCESS_KEY_ID") is not None and env("AWS_SECRET_ACCESS_KEY") is not None,
        reason="AWS credentials are set, skipping test",
    )
    def test_starting_task_with_correct_parameters(self, mock_encode_video):
        download_video(self.media.id)
        task: Task | None = Task.objects.filter(media=self.media).first()
        if task:
            mock_encode_video.assert_called_once_with(
                self.media.source_link,
                self.media.id,
                task.id,
            )

    @patch("kino.utils.stages_of_video.encoding.load_video.delay")
    def test_load_video_task(self, mock_load_video):
        task = Task.objects.create(
            media=self.media,
            status=StatusChoose.processing,
        )
        coding_video(self.media, task, self.quality, self.aspect_ratio)
        card_name: str | None = getattr(self.media.card, "name", None)
        if card_name:
            mock_load_video.assert_called_once_with(
                str(
                    Path(
                        settings.PATH_TO_MEDIA,
                        "tests",
                        card_name,
                        f"{self.quality}.mp4",
                    ),
                ),
                self.media.id,
                task.id,
            )
