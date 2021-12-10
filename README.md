# du03_vaclavtham

## Motivace
Chcete zhodnotit, jak jsou dostupné kontejnery na tříděný odpad v jednotlivých
čtvrtích. Proto chcete vědět, jaká je průměrná a maximální vzdálenost k
nejbližšímu kontejneru na tříděný odpad pro obyvatele dané čtvrti.

## Zadání
Pro zvolenou množínu adresních bodů a množinu kontejnerů na tříděný odpad
zjistěte průměrnou a maximální vzdálenost k nejbližšímu veřejnému kontejneru na
tříděný odpad. Pro každý adresní bod tedy určete nejbližší veřejný kontejner na
tříděný odpad a následně z těchto vzdáleností spočtěte průměr a maximum. Průměr
a maximum vypište, pro maximum vypište i adresu, která má nejbližší veřejný
kontejner nejdále. 

### Vstupní data
Vstupními daty budou 2 soubory GeoJSON. První obsahuje adresní body zvolené
čtvrti ve WGS-84, lze jej stáhnout z [Overpass
Turbo](http://overpass-turbo.eu/s/11rE) pomocí Exportovat -> Stáhnout jako
GeoJSON. V atributu `addr:street` naleznete jméno ulice, v atributu
`addr:housenumber` naleznete číslo orientační / číslo popisné. Soubor po stažení
pojmenujte `adresy.geojson` a pod tímto jménem ho program také bude načítat.

Druhý soubor obsahuje souřadnice kontejnerů na tříděný odpad, lze jej stáhnout z
[pražského Geoportálu](https://www.geoportalpraha.cz/cs/data/otevrena-data/8726EF0E-0834-463B-9E5F-FE09E62D73FB)
v S-JTSK. Každý kontejner obsahuje v atributu `STATIONNAME` adresu, kde se
nachází a v atributu `PRISTUP`, zda je veřejně přístupný, nebo je přístupný
pouze obyvatelům domu. Soubor po stažení pojmenujte `kontejnery.geojson` a pod
tímto jménem ho také program bude načítat.

### Výstup
Program vypíše, jaká je pro zvolenou množinu adres průměrná vzdálenost k
veřejnému kontejneru na tříděný odpad a ze které adresy je to k nejbližšímu
veřejnému kontejneru nejdále a jak daleko (v metrech, zaokrouhleno na cele
metry). Kontejnery, které jsou přístupné pouze obyvatelům domu nebudeme v
základní verzi uvažovat. Dále program může, ale nemusí, vypsat statistické
údaje o vstupních souborech, jako je počet adres a počet kontejnerů, tyto údaje
by měly být stručné a jasné a nic dalšího by program neměl vypisovat (pokud to
nepožaduje nějaký bonus).
### Další požadavky
Program by se měl vypořádat s nekorektním vstupem, jako je vadný nebo chybějící
vstupní soubor. Dále by program měl skončit s chybou, pokud pro některou adresu
je nejbližší kontejner dále než 10 km (může skončit ihned, nemusí dokončit
výpočet). Pokud je soubor validní JSON, ale nevalidní GeoJSON, nebo chybí nějaký
atribut, je v základní verzi v pořádku, že program spadne. 

## Bodování
 * 5 b za funkční aplikaci
 * 3 b za kvalitu kódu
 * 2 b za dokumentaci

Kvalita kódu nyní zahrnuje i komentáře v kódu, více o jednotlivých kategoriích v
minulém zadání.

## Bonusové body (které by měl splňovat tento program)

### Používání Gitu pro vývoj s vhodnými popisy commitů (1 b)
Pokud budete pro verzování používat Git, vytvořte si účet na GitHubu nebo jiné
podobné stránce a úkol můžete odevzdat přes něj. Kromě samotného odevzdání je
třeba, aby byl repozitář používán i pro vývoj, tedy by měl obsahovat průběžně
commitovanou práci a jednotlivé commity by měly obsahovat stručný a jasný popis
toho, co se v daném commitu změnilo. Repozitář by měl obsahovat jak program, tak
případný soubor s dokumentací, za hodnocenou verzi se počítá poslední commit
pushnutý na GitHub před deadlinem. Repozitář nemusí, ani by neměl, obsahovat
velká vstupní data.  Pokud budete potřebovat pomoct, pište mi.

### Medián (1 b)
Kromě průměrné vzdálenosti ke kontejneru vypište i [medián](https://cs.wikipedia.org/wiki/Medi%C3%A1n) vzdálenosti ke kontejneru. 

### Přiřazení kontejnerů k adresám (3 b)
Program vytvoří soubor `adresy_kontejnery.geojson` ve formátu GeoJSON, který
bude obsahovat všechny adresní body ze vstupních dat a v atributech každého
adresního bodu bude v klíči `kontejner` uloženo `ID` nejbližšího kontejneru k
danému adresnímu bodu.


## Popis programu

### Vytvoření funkcí
#### Načítání souboru
Pro načtění souboru je napsána funkce, která při načítání souboru ošetřuje zda soubor existuje, zda k němu má program přístup a zda je validní `FileNotFoundError`,`PermissionError`, `ValueError`.

#### Zjištění informací o kontejnerech
V této funkci přiřadí program do proměnných `ulice` `souradnice` `pristup` hodnoty z kontejnery.geojson. V podmínce zajistímě počítání pouze s veřejnými kontejnery, díky proměnné `pristup`. Pokud přístup není volný, tak přiřadí souřadnicím `None`

#### Zjištění informací o adresách domů
Přiřadí ulice a čísla domů do proměnné a také souřadnice daných míst z souboru adresy.geojson. A převede souřadnice pomocí `Transform` z WGS84 do souřadnicového systému JTSK.

#### Rozděluje čtení kontejnerů a adres
Dělí čtení kontejnerů a adres, ukládá je do datové struktury s klíčem reprezentujícím 
ulici a hodnotu reprezentující souřadnice. V této funkci je for cyklus, které projede jednotlivé adresy ptá se v podmínce zda je to kontejner či adresa domu. Také je tam dané výjimka v try bloku `KeyError`.
.
#### Výpočet vzdálenosti
Tato funkce pomocí pythagorovy věty vypočte vzdálenost bodů.

#### Hledá minimální vzdálenost ke kontejneru
Toto je vytvořeno jedním for cyklem, který projíždí adresy 
`for (adresa_ulice, adresa_souradnice) in adresy.items()` v tom je vnořený další for cyklus s kontejnery
`for kontejnery_ulice, kontejnery_souradnice in kontejnery.items()`, ve kterém jsou podmínky na ošetření kontejnerů bez souřadnic viz funkce Zjištění informací o kontejnerech a pokud mají stejnou ulici jako adresa, tak není minimální vzdálensot žádná. Následně vyvolá funkci na výpočet vzdálenosti a přiřadí vzdálenost do proměnné. Následuje podmínka přiřazení minimální vzdálenosti. V prvním cyklu adresy tzv. na stejné úrovni jako cyklus kontejnery následuje podmínka pro zajištění aby vzdálenost nesměla být větší než 10 km. A poté přiřazení do proměnné `vzdalenosti[adresa_ulice] = min_vzd`.

#### Medián (Bonus)
Vezme všechny hodnoty vzdáleností přiřadí je do seznamu, seřadí hodnoty a následně vypočítá medián vzdáleností

### Začátek programu
Do proměnných si přiřadíme soubory pomocí funkce `nacteni_souboru` soubory s adresami a kontejnery. Následně si pomocí funkce `nacteni_dat` načteme data z vytvořených proměných v předchozím kroku a přiřadímě do nových proměnných. V dalším kroku spočítám vzdálenosti `vzdalenosti = hledani_min_vzdalenosti(nacteni_kontejnery, nacteni_adresy)`, kde do funkce `hledani_min_vzdalenosti` použijeme předchozí proměnné, které jsme získaly z funkce načtení dat. Poté spočítáme průměr vzdáleností a medián. Následně pomocí funkce max zjistímě maximální vzdálenost ke kontejneru. Následně je proveden for cyklus pro zjištění adresy k maximální vzdálenosti, tím že porovnáme ve vzdálenost zda se vzdálenost rovná maximu. Poté následuje tisk výsledků.
