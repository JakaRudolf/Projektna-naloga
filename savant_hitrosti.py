import orodja

SEZONA = 2025
URL = f"https://baseballsavant.mlb.com/leaderboard/pitch-arsenals?year={SEZONA}&min=100&type=avg_speed&hand="
MAPA = "podatki/savant_hitrosti"
DATOTEKA = f"stran_savant_hitrosti_{SEZONA}.html"


# Prenese stran z lestvico in jo shrani, če še ne obstaja
def prenos_strani():
    if orodja.datoteka_obstaja(MAPA, DATOTEKA):
        print("stran je že prenesena, preskočim")
        return

    vsebina = orodja.prenesi_stran(URL)
    if vsebina is None:
        print("prenos ni uspel")
        return

    # Preverimo, ali stran res vsebuje podatke
    if "var data = [" not in vsebina:
        print("preneseni HTML ne vsebuje podatkov")
        return

    orodja.shrani_niz_v_datoteko(vsebina, MAPA, DATOTEKA)
    print("shranjeno:", DATOTEKA)


def main():
    prenos_strani()


if __name__ == "__main__":
    main()