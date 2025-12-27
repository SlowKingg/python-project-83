import requests
from bs4 import BeautifulSoup


def parse_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.string if soup.title else ""
    h1 = soup.h1.string if soup.h1 else ""
    description_tag = soup.find("meta", attrs={"name": "description"})
    description = (
        description_tag["content"]
        if description_tag and "content" in description_tag.attrs
        else ""
    )
    return {
        "title": title,
        "h1": h1,
        "description": description,
    }
