from urllib.parse import urlparse

import validators
from flask_babel import gettext


def normalize_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


def validate_url(url):
    if len(url) > 255:
        return gettext("Invalid URL")

    if not validators.url(url):
        return gettext("Invalid URL")
