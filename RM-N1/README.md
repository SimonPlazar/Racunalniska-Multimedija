# Vaja 1

V sklopu 1. vaje s poljubnim programskim jezikom implementirajte konzolno aplikacijo za stiskanje poljubnih datotek z aritmetičnim kodirnikom, ki temelji na skaliranju mej z uporabo napak E1, E2 in E3. Postopek je opisan v "Bodden et al., Arithmetic Coding revealed, 2007" in v priloženi predstavitvi.

Kodirnik naj bo 32-bitni. Način zapisa verjetnostne tabele je prepuščen vam. IO operacije morajo bit v binarnem načinu.

 

Vhod/izhod konzolne aplikacije (preko argumentov)

vaja1 <operacija> <vhodna datoteka> <izhodna datoteka>

kjer:

<operacija>:
c - kompresija
d - dekompresija
<vhodna datoteka> - pot do poljubne vhodne datoteke, ki jo odprete v binarnem načinu
<izhodna datoteka> - pot do izhodne datoteke, ki jo odprete v binarnem načinu
Primer uporabe:

vaja1 c test.txt test.comp

vaja1 c test.bmp test.comp

 

Poročilo

Poleg vaje prav tako pripravite in oddajte poročilo (1-2 strani max) v formatu PDF, kjer poročate naslednje ugotovitve:

Prikažite (graf ali tabela) kompresijskega razmerja za dane testne primere (glej test.zip).
Prikažite (graf ali tabela) časa kompresije za dane testne primere (glej test.zip).
Prikažite (graf ali tabela) časa dekompresije za dane testne primere (glej test.zip).
Z 2-5 stavki opišite kako ste kodirali tabelo verjetnosti.
Z 2-5 stavki opišite kako bi lahko pohitrili in optimizirali algoritem.
BONUS (do +5%): implementirajte predlagano optimizacijo in dodajte eno stran v poročilu, kjer prikažete spremembo v kompresijskem razmerju ter času kompresije/dekompresije pred in po optimizaciji. Izračunajte še faktor pohitritve (t.j. t_stari / t_novi).
 