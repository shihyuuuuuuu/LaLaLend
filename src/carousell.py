import enum
import os

import requests
from geopy.geocoders import Nominatim
from requests_html import HTMLSession

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from app.models import Supply
from app.schema import Category

# References:
# https://stackoverflow.com/questions/48163641/django-core-exceptions-appregistrynotready-apps-arent-loaded-yet-django-2-0/48168360
# https://stackoverflow.com/questions/1308386/programmatically-saving-image-to-django-imagefield


def parse_products(url):
    session = HTMLSession()
    r = session.get(url)
    if r.status_code != 200:
        print(f"Request {url} failed, status code: {r.status_code}")
        return []

    result = []
    for product in r.html.find(".D_rw.D_rr.D_sn"):
        username = product.find(".D_rG>p")[0].text
        info = product.find("a.D_b_")[1]
        p_url = main_url + info.attrs.get("href")
        r = session.get(p_url)
        try:
            location = r.html.find(".D_F .D_BQ .D_BS")[1].text
        except:
            print(f"{p_url} get location failed...")
            continue
        photo = r.html.find(".D_GT .D_GU img")[0].attrs["src"]
        infos = info.find("p")
        item = infos[0].text
        price = infos[1].text.split("NT$")[1].replace(",", "")
        description = infos[2].text

        result.append(
            {
                "username": username,
                "item": item,
                "location": location,
                "photo": photo,
                "price": price,
                "description": description,
            }
        )
    return result

geolocater = Nominatim(user_agent='lalalend')
main_url = "https://tw.carousell.com"
session = HTMLSession()
r = session.get(main_url)
assert r.status_code == 200, f"Request failed with status code {r.status_code}"
r.html.render()
categories = [c.value for c in Category]
target_urls = []
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}
default_long = 121.517005
default_lan = 25.047931

for category in r.html.find("a.D_sR.D_b_"):
    if category.text in categories:
        target_urls.append([main_url + category.attrs.get("href"), category.text])

for link, category in target_urls:
    result = parse_products(link)

    for r in result:
        location = geolocater.geocode(f"{r['location']}")
        product = Supply(
            user_id = "fake_user_id",
            username = r["username"],
            item = r["item"],
            category = category,
            location_long = location.longitude if location else default_long,
            location_lat = location.latitude if location else default_lan,
            description = r["description"],
            price = r["price"],
            line_id = "lalalend_official",
            phone_num = "0912345678"
        )

        url = r["photo"]
        filename = url.split("/")[-1]
        r = requests.get(url, headers=headers)
        with open(f'media/images/{filename}', 'wb') as outfile:
            outfile.write(r.content)
        product.photo = f'images/{filename}'
        product.save()
