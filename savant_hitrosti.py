import json
import re
import orodja

SEZONA = 2025
URL = f"https://baseballsavant.mlb.com/leaderboard/pitch-arsenals?year={SEZONA}&min=100&type=avg_speed&hand="
MAPA = "podatki/savant_hitrosti"
DATOTEKA = f"stran_savant_hitrosti_{SEZONA}.html"
CSV_DATOTEKA = f"savant_hitrosti_{SEZONA}.csv"

# Kratice vrst metov, kot jih uporablja Savant v imenih polj
VRSTE_METOV = ["ff", "si", "fc", "sl", "ch", "cu", "fs", "st", "sv"]

STOLPCI = [
    "id_metalca",
    "ime",
    "ekipa",
    "roka",
    "vrsta_meta",
    "delez",
    "hitrost",
    "vrtenje",
    "gibanje_x",
    "gibanje_z",
]


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


# Iz HTML-ja vzame seznam metalcev, ki je zapisan kot JSON v spremenljivki data
def izlusci_metalce(vsebina):
    ujemanje = re.search(r"var data = (\[.*?\]);\s*\n", vsebina, flags=re.DOTALL)
    return json.loads(ujemanje.group(1))


# Pretvori niz v število; prazne vrednosti (None ali "") postanejo None
def v_stevilo(vrednost):
    if vrednost is None or vrednost == "":
        return None
    return float(vrednost)


# Iz zapisa enega metalca naredi eno vrstico za vsako vrsto meta, ki jo meče
def vrstice_metalca(metalec):
    vrstice = []
    for vrsta in VRSTE_METOV:
        hitrost = v_stevilo(metalec.get(f"{vrsta}_avg_speed"))
        # Če metalec te vrste meta ne meče, vrstice ne naredimo
        if hitrost is None:
            continue
        vrstice.append(
            {
                "id_metalca": int(metalec["pitcher"]),
                "ime": metalec["name_display_first_last"],
                "ekipa": metalec["name_display_club"],
                "roka": metalec["pitch_hand"],
                "vrsta_meta": vrsta.upper(),
                "delez": v_stevilo(metalec.get(f"n_{vrsta}")),
                "hitrost": hitrost,
                "vrtenje": v_stevilo(metalec.get(f"{vrsta}_avg_spin")),
                "gibanje_x": v_stevilo(metalec.get(f"{vrsta}_avg_break_x")),
                "gibanje_z": v_stevilo(metalec.get(f"{vrsta}_avg_break_z_induced")),
            }
        )
    return vrstice


# Izvede celoten postopek: prenese stran, izlušči podatke in jih zapiše v CSV
def main():
    prenos_strani()

    vsebina = orodja.preberi_datoteko_v_niz(MAPA, DATOTEKA)
    metalci = izlusci_metalce(vsebina)

    vrstice = []
    for metalec in metalci:
        vrstice.extend(vrstice_metalca(metalec))

    orodja.zapisi_csv(STOLPCI, vrstice, MAPA, CSV_DATOTEKA)
    print("metalcev:", len(metalci), "| vrstic v CSV:", len(vrstice))


if __name__ == "__main__":
    main()