import pandas as pd
from pathlib import Path
import seaborn as sns

# Pfad zu Arbeitsverzeichnis
PATH_WD = Path(__file__).parent

# Pfad zu Daten
PATH_BRUTTOINLANDSPRODUKT = PATH_WD / "daten/bruttoinlandsprodukt_bundeslaender_bearbeitet.xlsx"
PATH_LEBENSERWARTUNG = PATH_WD / "daten/lebenserwartung_bundeslaender.csv"

# Daten einlesen Bruttoinlandsprodukt
df_bruttoinlandsprodukt = pd.read_excel(PATH_BRUTTOINLANDSPRODUKT, dtype={})
df_bruttoinlandsprodukt = df_bruttoinlandsprodukt[df_bruttoinlandsprodukt["Land"] == "Brandenburg"].reset_index(drop=True)
for year in range(2008, 2024):
    df_bruttoinlandsprodukt[year] = df_bruttoinlandsprodukt[year].astype("Float64")
#print(df_bruttoinlandsprodukt)
#print(df_bruttoinlandsprodukt.info())

# Daten einlesen Lebenserwartung
df_lebenserwartung = pd.read_csv(PATH_LEBENSERWARTUNG, nrows=238, sep=";")#, dtype={"Frauen": "Float64", "Maenner":"Float64"})
df_lebenserwartung["Maenner"] = df_lebenserwartung["Maenner"].apply(lambda x: x.replace(",", ".")).astype("Float64")
df_lebenserwartung["Frauen"] = df_lebenserwartung["Frauen"].apply(lambda x: x.replace(",", ".")).astype("Float64")
#print(df_lebenserwartung)
#print(df_lebenserwartung.info())

# Nach Daten fuer Brandenburg sortieren
df_lebenserwartung = df_lebenserwartung[df_lebenserwartung["Laenderschluessel"] == 12].reset_index(drop=True)
#print(df_lebenserwartung)

# "Statistik", "Laenderschluessel" und "Bundesland" entfernen
df_lebenserwartung = df_lebenserwartung.drop(columns=["Statistik", "Laenderschluessel", "Bundesland"])
#print(df_lebenserwartung)

# Durschnittliches BIP fuer den gegebenen Zeitraum and Lebenserwartungsdatensatz anfuegen
def helper_bip(yrs:str):
    # Liste mit einzelnen Jahren aus einem String des Formats "Jahr1/Jahr2"
    yrs = yrs.split("/")
    # Definiere Eine pd.Series, welche die einzelnen Jahre in dem gegebnen Zeitraum enthaelt
    yrs_range = pd.Series((range(int(yrs[0]), int(yrs[1]) + 1)))
    # Berechne den Mittelwert des BIP fuer die betreffenden Jahre
    mean_bip = df_bruttoinlandsprodukt[yrs_range].mean(axis=1)[0]
    return mean_bip

df_lebenserwartung["durschnittlichesBIP"] = df_lebenserwartung["Jahr"].apply(helper_bip)
# Korrelation berechnen zwischen Lebenserwartung und BIP fuer Frauen und Maenner
Korrelationen = df_lebenserwartung[["Frauen", "Maenner", "durschnittlichesBIP"]].corr()
print("Korrlelation zwischen der Lebenserwartung von Maennern und BIP: ", Korrelationen["Maenner"]["durschnittlichesBIP"])
print("Korrlelation zwischen der Lebenserwartung von Frauen und BIP: ", Korrelationen["Frauen"]["durschnittlichesBIP"])

# Grafik, welche die Entwicklung von BIP und Lebenserwartungen über die Zeit zeigt
sns.lineplot(data=df_lebenserwartung, x="Jahr", y=["Frauen", "Maenner", "durschnittlichesBIP"])
