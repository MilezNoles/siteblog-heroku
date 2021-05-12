from django import template
import requests
from bs4 import BeautifulSoup

register = template.Library()





@register.inclusion_tag("blog/currency.html")
def check_currency():
    DOLLAR_RUB = "https://www.google.com/search?q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&newwindow=1&sxsrf=ALeKk02azXQ2fV4VAjpWTAEQTDGQR2YoWQ%3A1618169919837&ei=P1BzYPmdMs-JrwTBrpPADA&oq=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+&gs_lcp=Cgdnd3Mtd2l6EAEYATIFCAAQywEyBQgAEMsBMgUIABDLATIFCAAQywEyBQgAEMsBMgUIABDLATIFCAAQywEyBQgAEMsBMgUIABDLATIFCAAQywE6BwgjEOoCECc6CQguEOoCECcQEzoGCCMQJxATOgQIIxAnOgIIADoICC4QxwEQowI6AgguOgQILhAnUJqjAVjGsQFgysABaAFwAngAgAF0iAHBBJIBAzcuMZgBAKABAaoBB2d3cy13aXqwAQrAAQE&sclient=gws-wiz"
    BITCOIN_RUB = "https://www.google.com/search?q=%D0%B1%D0%B8%D1%82%D0%BA%D0%BE%D0%B8%D0%BD+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&newwindow=1&sxsrf=ALeKk02PkcD5FSljmsB20-JY-jKyra1IUA%3A1618169945560&ei=WVBzYLeSIfCTwPAP7P2f0AU&oq=%2Cbnrjby+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp=Cgdnd3Mtd2l6EAEYADIECAAQDTIGCAAQDRAeMgYIABANEB4yBggAEA0QHjIGCAAQDRAeMgYIABANEB4yBggAEA0QHjIGCAAQDRAeMgYIABANEB4yBggAEA0QHjoGCAAQBxAeOgUIABDLAToECAAQEzoICAAQBxAeEBM6CggAEA0QBRAeEBM6CggAEAgQDRAeEBM6CggAEAcQChAeEBM6CggAEAcQBRAeEBM6CggAEAcQChAeECpQub_xAVj5yfEBYIDT8QFoAHACeACAAacBiAGvBJIBAzcuMZgBAKABAqABAaoBB2d3cy13aXrAAQE&sclient=gws-wiz"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}

    full_page_usd = requests.get(DOLLAR_RUB, headers=headers)
    full_page_btc = requests.get(BITCOIN_RUB, headers=headers)

    soup_usd = BeautifulSoup(full_page_usd.content, "html.parser")
    soup_btc = BeautifulSoup(full_page_btc.content, "html.parser")

    USD_to_RUB = soup_usd.find("span", class_="SwHCTb").get_text(strip=True)
    BTC_to_RUB = soup_btc.find("span", class_="SwHCTb").get_text(strip=True)

    return {"USD_to_RUB": USD_to_RUB, "google_link_usd": DOLLAR_RUB,
            "BTC_to_RUB": BTC_to_RUB, "google_link_btc": BITCOIN_RUB,
            }