# du03_vaclavtham

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
