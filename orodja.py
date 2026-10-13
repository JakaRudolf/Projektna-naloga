import os
import requests

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def prenesi_stran(url):
    try:
        odgovor = requests.get(url, headers=HEADERS, timeout=30)
        odgovor.raise_for_status()
    except requests.exceptions.RequestException as napaka:
        print("spletna stran ni dosegljiva:", napaka)
        return None
    return odgovor.text


def shrani_niz_v_datoteko(besedilo, mapa, datoteka):
    os.makedirs(mapa, exist_ok=True)
    pot = os.path.join(mapa, datoteka)
    with open(pot, "w", encoding="utf-8") as izhod:
        izhod.write(besedilo)