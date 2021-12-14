import json,argparse
from pyproj import CRS, Transformer
from math import sqrt
from sys import exit

# Určím cestu relativní cestu ke konterjnerům a adresám
cesta_kontejnery = "kontejnery.geojson"
cesta_adresy = "adresy.geojson"

wgs2jtsk = Transformer.from_crs(CRS.from_epsg(4326), CRS.from_epsg(5514))


# Bonus, ktery nacte soubor jako parametr za pomoci modulu Argparse.
parser = argparse.ArgumentParser()
parser.add_argument('-a', '--adresy', type = str, required=False, default=None)
parser.add_argument('-k', '--kontejnery', type = str, required=False, default=None)
args = parser.parse_args()
if args.adresy != None:
    cesta_adresy = args.adresy
elif args.kontejnery != None:
    cesta_kontejnery = args.kontejnery

def nacteni_souboru(nazev):
    """Načtení souboru a oveření, zda soubor existuje a program má k němu přístup."""
    try:
        with open(nazev, "r", encoding="UTF-8") as soubor:
            return json.load(soubor)["features"]
    except FileNotFoundError:
        print(f"Soubor {nazev} neexistuje.")
        exit()
    except PermissionError:
        print(f"Program nemá přístup k {nazev}.")
        exit()
    except ValueError as e:
        print(f"Soubor {nazev} není validní.\n", e)
        exit()
        
def cteni_kontejneru(misto):
    """Přiřadí do proměnných potřebné informace z kontejnery.geojson. 
    V podmínce zajistímě počítání pouze s veřejnými kontejnery"""
    ulice = misto["properties"]["STATIONNAME"]
    souradnice = misto["geometry"]["coordinates"]
    pristup = misto["properties"]["PRISTUP"]

    if pristup=="volně":
        return ulice, souradnice
    elif pristup=="obyvatelům domu":
        return ulice, None

def cteni_adresy(misto):
    """Přiřadí ulice a čísla domů do proměnné a také souřadnice daných míst."""
    ulice = misto["properties"]["addr:street"] + " " + misto["properties"]["addr:housenumber"]
    souradnice_sirka = misto["geometry"]["coordinates"][1]
    souradnice_delka = misto["geometry"]["coordinates"][0]

    return ulice, wgs2jtsk.transform(souradnice_sirka, souradnice_delka)

def nacteni_dat(data, kontejner=True):
    """Načte a umí zpracovávat jak kontejnery a adresy, podle hodnoty parametru kontejner, ukládá je do datové struktury s klíčem reprezentujícím 
    ulici a hodnotu reprezentující souřadnice"""
    nacteni = {}
    for misto in data:
        try:
            if kontejner:
                ulice, souradnice = cteni_kontejneru(misto)
            else:
                ulice, souradnice = cteni_adresy(misto)
            
            nacteni[ulice] = souradnice
        except KeyError:
            print("Klíč který hledáte nebyl nalezen")
            pass

    nazev = "kontejneru"
    if kontejner==False:
        nazev = "adres"

    if len(nacteni)==0:
        print(f"Není k dispozici dostatečný počet dat pro výpočet (u {nazev}).")
        exit()

    return (nacteni)
    
def pythagoras(s1, s2):
    """Vypocet vzdalenosti bodu pomoci Pythagorovy vety."""
    return sqrt((s1[0] - s2[0])**2 + (s1[1] - s2[1])**2)

def hledani_min_vzdalenosti(kontejnery, adresy):
    """ Hleda minimalni vzdalenost od kontejneru."""
    vzdalenosti = {}
    
    for (adresa_ulice, adresa_souradnice) in adresy.items():

        min_vzd = float('inf')

        for kontejnery_ulice, kontejnery_souradnice in kontejnery.items():
            if kontejnery_souradnice==None and kontejnery_ulice==adresa_ulice:
                min_vzd = 0
                break
            if kontejnery_souradnice==None:
                continue
            
            vzdalenost = pythagoras(adresa_souradnice, kontejnery_souradnice)
            if vzdalenost < min_vzd:
                min_vzd = vzdalenost

        if min_vzd > 10000: # Ošetření, že vzdálenost musí být menší než 10 km
            print("Kontejner je dál než 10 km.")
            exit()

        vzdalenosti[adresa_ulice] = min_vzd

    return vzdalenosti

def median(vzdalenosti):

    sez_vzdalenosti = list(vzdalenosti.values())
    sez_vzdalenosti.sort()
    p = (len(sez_vzdalenosti) - 1) // 2

    # kdyz vyjde zbytek po vypoctu 0, program vypise false
    # kdyz vyjde zbytek po vypoctu 1, program vypise true
    if len(sez_vzdalenosti) % 2:
        return sez_vzdalenosti[p]

    return (sez_vzdalenosti[p] + sez_vzdalenosti[p + 1]) / 2


data_kontejnery = nacteni_souboru(cesta_kontejnery)
data_adresy = nacteni_souboru(cesta_adresy)

nacteni_kontejnery = nacteni_dat(data_kontejnery)

nacteni_adresy = nacteni_dat(data_adresy, False)

vzdalenosti = hledani_min_vzdalenosti(nacteni_kontejnery, nacteni_adresy)

prumer = sum(vzdalenosti.values()) / len(vzdalenosti)

median = median(vzdalenosti)

maximum = max(vzdalenosti.values())

for (adresa, vzdalenost) in vzdalenosti.items():
    if vzdalenost == maximum:
        nejvzdalenejsi = adresa

# Výpis výsledků

print()
print(f"Načteno adresních bodů: {len(nacteni_adresy)}")
print(f"Načteno kontejnerů na tříděný odpad: {len(nacteni_kontejnery)}")
print()
print(f"Průměrná vzdálenost adresního bodu ke kontejneru: "f"{prumer:.0f}"" metrů")
print(f"Median vzdálenosti ke kontejneru: {median:.0f} metru")
print()
print(f"Nejdále ke kontejneru je z adresního bodu '{nejvzdalenejsi}', konkrétně {maximum:.0f} metrů")