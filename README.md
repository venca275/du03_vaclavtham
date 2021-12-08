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

## Bonusové body

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

