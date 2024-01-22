import requests
from requests import RequestException
from bs4 import BeautifulSoup


request_error = RequestException


def get_response(url):
    return requests.get(url, timeout=(3.05, 10))


def get_status_code(response):
    response.raise_for_status()
    return response.status_code


def get_h1_title_desc(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    h1 = soup.h1.text if soup.h1 else ''
    title = soup.title.text if soup.title else ''
    desc_with_tag = soup.find('meta', {'name': 'description'})
    desc = desc_with_tag['content'] if desc_with_tag else ''
    desc = desc if len(desc) < 255 else desc[:252] + '...'
    return h1, title, desc


def get_seo_data(url):
    resopnse = get_response(url)
    h1, title, desc = get_h1_title_desc(resopnse)
    status_code = get_status_code(resopnse)
    return h1, title, desc, status_code
