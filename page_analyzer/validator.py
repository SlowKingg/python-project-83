from urllib.parse import urlparse

import validators
from flask_babel import gettext


def normalize_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


def validate_url(url):
    if not validators.url(url) or len(url) > 255:
        return gettext("Invalid URL")

    return None
