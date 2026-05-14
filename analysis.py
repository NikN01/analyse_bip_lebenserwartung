import pandas as pd
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt

# Pfad zu Arbeitsverzeichnis
PATH_WD = Path(__file__).parent

# Pfad zu Daten
PATH_BRUTTOINLANDSPRODUKT = PATH_WD / "daten/bruttoinlandsprodukt_bundeslaender_bearbeitet.xlsx"
PATH_LEBENSERWARTUNG = PATH_WD / "daten/lebenserwartung_bundeslaender.csv"

# Daten einlesen Bruttoinlandsprodukt
df_bruttoinlandsprodukt = pd.read_excel(PATH_BRUTTOINLANDSPRODUKT, dtype={"Land":pd.StringDtype()})
df_bruttoinlandsprodukt = df_bruttoinlandsprodukt[df_bruttoinlandsprodukt["Land"] == "Brandenburg"].reset_index(drop=True)
for year in range(2008, 2024):
    df_bruttoinlandsprodukt[year] = df_bruttoinlandsprodukt[year].astype("Float64")
print(df_bruttoinlandsprodukt)
print(df_bruttoinlandsprodukt.info())

assert df_bruttoinlandsprodukt.isnull().values.any() == False
assert df_bruttoinlandsprodukt.duplicated().values.any() == False

# Daten einlesen Lebenserwartung
df_lebenserwartung = pd.read_csv(PATH_LEBENSERWARTUNG, nrows=238, sep=";", dtype={
    "Laenderschluessel":int, "Bundesland":pd.StringDtype(), "Jahr":pd.StringDtype()
})
df_lebenserwartung["Maenner"] = df_lebenserwartung["Maenner"].apply(lambda x: x.replace(",", ".")).astype("Float64")
df_lebenserwartung["Frauen"] = df_lebenserwartung["Frauen"].apply(lambda x: x.replace(",", ".")).astype("Float64")
print(df_lebenserwartung)
print(df_lebenserwartung.info())

assert df_lebenserwartung.isnull().values.any() == False
assert df_lebenserwartung.duplicated().values.any() == False

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
fig, ax1 = plt.subplots()
# Füge 2. Y-Achse hinzu
ax2= ax1.twinx()

# Grafik für Lebenserwartungen von Frauen und Männern
sns.lineplot(data=df_lebenserwartung, x="Jahr", y="Frauen", ax=ax1, color="red")
sns.lineplot(data=df_lebenserwartung, x="Jahr", y="Maenner", ax=ax1, color="blue").set(
    ylabel="Lebenserwartung(Jahr)",
    xlabel = "Jahr",
    title="Lebenserwartung vs. BIP",
)

# Grafik für BIP
sns.lineplot(data=df_lebenserwartung, x="Jahr", y="durschnittlichesBIP", ax=ax2, color="black").set(
    ylabel="BIP(Mrd. Euro)"
)

# Rotiere x-Werte
ax1.tick_params(axis="x", rotation=45)
# Fuege Legende hinzu
ax1.legend(handles = ax1.get_lines()+ax2.get_lines(), 
           labels=["Lebenserwartung Frauen", "Lebenserwartung Männer","BIP"],
           loc="lower right")
# Aendere Reihenfolge der x-Werte
ax1.xaxis.set_inverted(True)
# Setze die Grenzen der y-Werte für beide Y-Achsen
ax1.set_ylim(ymin=0, ymax=100)
ax2.set_ylim(ymin=0, ymax=100)
# Passe Höhe der Grafik an
fig.set_figheight(fig.get_figheight() + 2.5)

plt.show()

