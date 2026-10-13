import csv
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


def preberi_datoteko_v_niz(mapa, datoteka):
    pot = os.path.join(mapa, datoteka)
    with open(pot, "r", encoding="utf-8") as vhod:
        return vhod.read()


def datoteka_obstaja(mapa, datoteka):
    return os.path.exists(os.path.join(mapa, datoteka))


def zapisi_csv(stolpci, vrstice, mapa, datoteka):
    os.makedirs(mapa, exist_ok=True)
    pot = os.path.join(mapa, datoteka)
    with open(pot, "w", encoding="utf-8", newline="") as csv_datoteka:
        pisatelj = csv.DictWriter(csv_datoteka, fieldnames=stolpci)
        pisatelj.writeheader()
        for vrstica in vrstice:
            pisatelj.writerow(vrstica)