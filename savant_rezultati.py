import random
import time
import orodja

SEZONA = 2025
VRSTE_METOV = ["FF", "SI", "FC", "SL", "CH", "CU", "FS", "ST", "SV"]
URL = "https://baseballsavant.mlb.com/leaderboard/pitch-arsenal-stats?type=pitcher&pitchType={}&year={}&team=&min=100"
MAPA = "podatki/savant_rezultati"


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


def main():
    prenos_strani()


if __name__ == "__main__":
    main()