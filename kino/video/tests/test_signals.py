from unittest.mock import patch

from factory import Faker

from kino.video.tests.utils.base_video import BaseVideoCard


class TestMediaSignals(BaseVideoCard):
    def test_create_media_signal(self):
        self.assertTrue(
            self.media,
            f"Media: {self.media}",
        )

    def test_download_media_signal(self):
        self.media.source_link = Faker("url")

        with patch("kino.video.tasks.download_video.delay") as mock_download_video:
            self.media.save()
            mock_download_video.assert_called_once_with(self.media.id)
