import orodja

URL = "https://baseballsavant.mlb.com/leaderboard/pitch-arsenals?year=2025&min=100&type=avg_speed&hand="
vsebina = orodja.prenesi_stran(URL)

if vsebina is not None:
    print("dolžina:", len(vsebina))
    print("najde Skubal:", "Skubal" in vsebina)
    orodja.shrani_niz_v_datoteko(vsebina, "podatki/savant_hitrosti", "test.html")