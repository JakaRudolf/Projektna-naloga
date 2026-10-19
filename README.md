# Vpliv hitrosti in vrste meta na odbijanje v MLB

Projektna naloga pri predmetu Uvod v programiranje.

## Opis

V nalogi preučujem, kako hitrost in vrsta meta v ligi MLB vplivata na to, kako
odbijalec žogo odbije (zgrešen zamah, hitrost odboja, povprečje udarcev).

Podatki so s strani [Baseball Savant](https://baseballsavant.mlb.com/) (Statcast)
za sezono 2025, samo redni del sezone (brez končnice).

## Vir podatkov

Uporabljam dve lestvici:

- **Pitch Arsenals** (hitrosti): za vsakega metalca povprečna hitrost, vrtenje in
  gibanje vsake vrste meta.
- **Pitch Arsenal Stats** (rezultati): za vsakega metalca in vrsto meta, kaj so
  odbijalci dosegli proti njej. Ena stran za vsako vrsto meta (9 strani).

Upoštevani so samo meti, ki jih je metalec vrgel vsaj 100-krat.

## Struktura repozitorija

- `orodja.py`: pomožne funkcije (prenos strani, shranjevanje datotek, zapis CSV)
- `savant_hitrosti.py`: prenese lestvico hitrosti in iz nje zapiše CSV
- `savant_rezultati.py`: prenese 9 lestvic rezultatov in iz njih zapiše CSV
- `podatki/`: shranjene HTML strani in pridobljena CSV-ja
  - `savant_hitrosti/savant_hitrosti_2025.csv`
  - `savant_rezultati/savant_rezultati_2025.csv`
- `analiza.ipynb`: analiza podatkov z grafi in komentarji

## Navodila za zagon

1. Namesti potrebne knjižnice:

       pip install requests pandas matplotlib

2. Zaženi obe skripti (če HTML strani že obstajajo, se ne prenašajo ponovno):

       python savant_hitrosti.py
       python savant_rezultati.py

3. Odpri `analiza.ipynb` (npr. v VS Code) in zaženi vse celice.

## Glavne ugotovitve

- Hitri meti (four-seam fastball, sinker) imajo najmanj zgrešenih zamahov,
  počasnejši meti z več gibanja (slider, curveball, splitter) pa približno dvakrat več.
- Pri four-seam fastballih hitrejši met pomeni več zgrešenih zamahov,
  na hitrost odboja pa hitrost skoraj ne vpliva.

## Uporaba umetne inteligence

Pri pisanju kode in razlagi korakov mi je pomagal Claude (Anthropic).