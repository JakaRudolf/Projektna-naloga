import orodja

URL = "https://baseballsavant.mlb.com/leaderboard/pitch-arsenal-stats?type=pitcher&pitchType=FF&year=2025&team=&min=100"
vsebina = orodja.prenesi_stran(URL)

if vsebina is not None:
    print("dolžina:", len(vsebina))
    print("najde Skubal:", "Skubal" in vsebina)
    orodja.shrani_niz_v_datoteko(vsebina, "podatki/savant_hitrosti", "test.html")