import csv #besedilna datoteka, shranjevanje podatkov v obliki tabele
import os
import requests

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def prenesi_stran(url):
    try:
        odgovor = requests.get(url, headers=HEADERS, timeout=30) #poslje zahtevo strezniku (ce ni odgovora v 30s odneha)
        odgovor.raise_for_status() #preveri,ce je v redu -- koda stanja = 200
    except requests.exceptions.RequestException as napaka:
        print("spletna stran ni dosegljiva:", napaka)
        return None
    return odgovor.text
#vrne html kodo kot besedilo


def shrani_niz_v_datoteko(besedilo, mapa, datoteka):
    os.makedirs(mapa, exist_ok=True)
    pot = os.path.join(mapa, datoteka)
    with open(pot, "w", encoding="utf-8") as izhod:
        izhod.write(besedilo) 
#shrani vsebino strani v datoteko, hkrati jo s pomocjo os pravilno razvrsti
#ce mapa ne obstaja jo ustvari

def preberi_datoteko_v_niz(mapa, datoteka):
    pot = os.path.join(mapa, datoteka)
    with open(pot, "r", encoding="utf-8") as vhod:
        return vhod.read()
#obratno, shrani datoteko v niz

def datoteka_obstaja(mapa, datoteka):
    return os.path.exists(os.path.join(mapa, datoteka))
#zagotovi da se stran ne prenese vsakic ko zazenemo skripto
#stran se lahko spremeni, to zagotovi da so podatki vedno isti

def zapisi_csv(stolpci, vrstice, mapa, datoteka):
    os.makedirs(mapa, exist_ok=True)
    pot = os.path.join(mapa, datoteka)
    with open(pot, "w", encoding="utf-8", newline="") as csv_datoteka:
        pisatelj = csv.DictWriter(csv_datoteka, fieldnames=stolpci)
        pisatelj.writeheader()
        for vrstica in vrstice:
            pisatelj.writerow(vrstica)
#newline (windows only) prepreci nastanek praznih vrstic
#writerow --> en slovar ena vrstica
#vrstice je seznam slovarjev (en slovar = ena vrstica)
#dobi imena stolpcev in seznam slovarjev -> vse zapise v csv datoteko