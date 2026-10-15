import json
import random
import re
import time
import orodja

SEZONA = 2025
VRSTE_METOV = ["FF", "SI", "FC", "SL", "CH", "CU", "FS", "ST", "SV"]
URL = "https://baseballsavant.mlb.com/leaderboard/pitch-arsenal-stats?type=pitcher&pitchType={}&year={}&team=&min=100"
MAPA = "podatki/savant_rezultati"
CSV_DATOTEKA = f"savant_rezultati_{SEZONA}.csv"

# Stolpci v CSV: ime stolpca -> ime polja v podatkih Savanta
STOLPCI = {
    "id_metalca": "player_id",
    "vrsta_meta": "pitch_type",
    "pa": "pa",
    "meti": "pitches",
    "ba": "ba",
    "woba": "woba",
    "k_odstotek": "k_percent",
    "whiff": "whiff_percent",
    "hitrost_odboja": "exit_velocity_avg",
    "kot_odboja": "launch_angle_avg",
    "hard_hit": "hard_hit_percent",
    "sweet_spot": "sweet_spot_percent",
    "barrel": "barrel_batted_rate",
}


def ime_datoteke(vrsta):
    return f"stran_savant_rezultati_{vrsta}_{SEZONA}.html"


# Za vsako vrsto meta prenese stran z rezultati in jo shrani
def prenos_strani():
    for vrsta in VRSTE_METOV:
        datoteka = ime_datoteke(vrsta)

        # že prenesene strani preskočimo
        if orodja.datoteka_obstaja(MAPA, datoteka):
            continue

        vsebina = orodja.prenesi_stran(URL.format(vrsta, SEZONA))
        if vsebina is None:
            print("prenos ni uspel:", vrsta)
            continue

        # stran mora vsebovati podatke in pravo vrsto meta
        if "var leaderboardData = [{" not in vsebina:
            print("stran nima podatkov:", vrsta)
            continue
        if f'"pitchType":"{vrsta}"' not in vsebina:
            print("stran ni za vrsto meta", vrsta)
            continue

        orodja.shrani_niz_v_datoteko(vsebina, MAPA, datoteka)
        print("shranjeno:", datoteka)

        # premor, da strežnika ne obremenjujemo
        time.sleep(random.uniform(2, 3))


# Iz HTML-ja vzame seznam metalcev, ki je zapisan kot JSON v spremenljivki leaderboardData
def izlusci_vrstice(vsebina):
    ujemanje = re.search(r"var leaderboardData = (\[.*?\]);", vsebina, flags=re.DOTALL)
    return json.loads(ujemanje.group(1))


# Pretvori niz v število; prazne vrednosti (None ali "") postanejo None
def v_stevilo(vrednost):
    if vrednost is None or vrednost == "":
        return None
    return float(vrednost)


# Iz zapisa Savanta naredi vrstico z imeni stolpcev, ki jih uporabljamo
def pocisti_vrstico(zapis):
    vrstica = {}
    for stolpec, polje in STOLPCI.items():
        if stolpec == "vrsta_meta":
            vrstica[stolpec] = zapis[polje]
        elif stolpec in ("id_metalca", "pa", "meti"):
            vrstica[stolpec] = int(zapis[polje])
        else:
            vrstica[stolpec] = v_stevilo(zapis[polje])
    return vrstica


# Izvede celoten postopek: prenese strani, izlušči podatke in jih zapiše v CSV
def main():
    prenos_strani()

    vrstice = []
    for vrsta in VRSTE_METOV:
        datoteka = ime_datoteke(vrsta)
        if not orodja.datoteka_obstaja(MAPA, datoteka):
            print("manjka datoteka:", datoteka)
            continue
        vsebina = orodja.preberi_datoteko_v_niz(MAPA, datoteka)
        for zapis in izlusci_vrstice(vsebina):
            vrstice.append(pocisti_vrstico(zapis))

    orodja.zapisi_csv(list(STOLPCI.keys()), vrstice, MAPA, CSV_DATOTEKA)
    print("vrstic v CSV:", len(vrstice))


if __name__ == "__main__":
    main()