import requests
import responses
from django.conf import settings


def mock_api_to_imdb(id_imdb):
    url_to_imdb = settings.IMDB_API + id_imdb
    response_body = {"imdbRating": 9.3}
    with responses.RequestsMock() as resp:
        resp.add(responses.GET, url_to_imdb, json=response_body, status=200)
        response = requests.get(url_to_imdb, timeout=15)
        data = response.json()
        return float(data["imdbRating"])
