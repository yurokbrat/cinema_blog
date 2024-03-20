import re

from kino.cards.models import Film


def get_media_folders(media):
    directory_name = re.sub(r'[:"/\\|?*]', '', media.card.name)
    content_type_model = media.content_type.model_class()
    content_type_folder = "films" if content_type_model == Film else "serials"
    if media.season:
        directory_name = f"{directory_name}/season_{media.season}"
        if media.episode:
            directory_name = f"{directory_name}/episode_{media.episode}"
    return directory_name, content_type_folder
