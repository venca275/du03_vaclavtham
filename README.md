# du03_vaclavtham

## Uživatelská dokumentace
Při spuštění programu a předání parametrů -a či -k s názvy souboru má možnost uživatel určit vlastní GEOJSON soubory. Pokud uživatel nepředá název souboru, program využije předem definované názvy. Program očekává, že soubor s adresami bude v souřadnicovém systému WGS84 a kontejnery v JTSK. Příklad vsutpu adres
```
      {
        "type": "Feature",
        "properties": {
          "@id": "node/296443235",
          "addr:conscriptionnumber": "333",
          "addr:housenumber": "333/25",
          "addr:postcode": "14800",
          "addr:street": "Volarská",
          "addr:streetnumber": "25",
          "source:addr": "uir_adr",
          "uir_adr:ADRESA_KOD": "21878757"
        },
        "geometry": {
          "type": "Point",
          "coordinates": [
            14.4851432,
            50.0101681
          ]
        },
        "id": "node/296443235"
      },
```
Příklad vstupu kontejnerů
```
	{
			"type" : "Feature",
			"geometry" : {
				"type" : "Point",
				"coordinates" : [ -741687.4500369802, -1044981.8600061499 ]
			},
			"properties" : {
				"OBJECTID" : 1,
				"ID" : 5597,
				"STATIONNUMBER" : "0002/-477",
				"STATIONNAME" : "Máchova 1137/8",
				"CITYDISTRICTRUIANCODE" : 500089,
				"CITYDISTRICT" : "Praha 2",
				"PRISTUP" : "obyvatelům domu"
			}
		},
```
Program spočítá kolik bylo načteno adresních bodů, kolik bylo načteno kontejnerů. Poté také průměrnou vzdálenost adresního bodu ke kontejneru. Medián vzdálenosti k nejbližšímu kontejneru. A také jaké adresa to má k nejbližšímu kontejneru nejdále. A tyto údaje vypíše do terminálu.

## Popis programu

### Vytvoření funkcí
#### Načítání souboru
Pro načtění souboru je napsána funkce, která při načítání souboru ošetřuje zda soubor existuje, zda k němu má program přístup a zda je validní `FileNotFoundError`,`PermissionError`, `ValueError`.

#### Zjištění informací o kontejnerech
V této funkci program zjistí hodnoty `ulice` `souradnice` `pristup` z kontejnery.geojson. Zajistí počítání pouze s veřejnými kontejnery. Pokud přístup není volný, tak jsou souřadnice `None`

#### Zjištění informací o adresách domů
Funkce zjistí ulice a čísla domů a také souřadnice daných míst z souboru adresy.geojson. A převede souřadnice pomocí `Transform` z WGS84 do souřadnicového systému JTSK.

#### Rozděluje čtení kontejnerů a adres
Umí zpracovávat data kontejnerů a adres podle hodnoty parametru, ukládá je do datové struktury s klíčem reprezentujícím ulici a hodnotu reprezentující souřadnice. V této funkci projede jednotlivé adresy ptá se v podmínce zda je to kontejner či adresa domu. Také je tam daná výjimka `KeyError`, což znamená, že klíč který hledáme nebyl nalezen.

#### Výpočet vzdálenosti
Tato funkce pomocí pythagorovy věty vypočte vzdálenost bodů.

#### Hledá minimální vzdálenost ke kontejneru
Funkce projíždí adresy v tom je vnořený cyklus s kontejnery, ve kterém jsou podmínky na ošetření kontejnerů bez souřadnic viz funkce Zjištění informací o kontejnerech a pokud mají stejnou ulici jako adresa, tak je minimální vzdálenost nulová. Následně vyvolá funkci na výpočet vzdálenosti. Následuje podmínka přiřazení minimální vzdálenosti. V prvním cyklu adresy tzv. na stejné úrovni jako cyklus kontejnery následuje podmínka pro zajištění aby minimální vzdálenost nebyla být větší než 10 km.

#### Medián
Vezme všechny hodnoty vzdáleností ze seznamu, seřadí hodnoty a následně vypočítá medián vzdáleností

### Začátek programu
Načteme si soubory pomocí funkce `nacteni_souboru` soubory s adresami a kontejnery. Následně si pomocí funkce `nacteni_dat` načteme data z předchozí funkce. V dalším kroku spočítám vzdálenosti, kde do funkce `hledani_min_vzdalenosti` použijeme předchozí hodnoty, které jsme získaly z funkce načtení dat. Poté spočítáme průměr vzdáleností a medián a maximální vzdálenost. Poté následuje tisk výsledků.
