# Domača naloga 1

V sklopu 1. domače naloge s poljubnim programskim jezikom implementirajte konzolno aplikacijo za osnovno urejanje binarnih datotek. Aplikacija naj omogoča naslednje osnovne I/O operacije:

 

- Binarni zapis ali branje zaporedja bitov.

- Binarni zapis ali branje posameznih bitov.

 

Na podlagi zgornjih operacij implementirajte naslednje funkcionalnosti:

 
- Iskanje zaporedja bitov (brez prepletanja) v vhodni binarni datoteki ter izpis pozicije bita v datoteki. V primeru več zadetkov iskanja izpišite vsako pozicijo ločeno s presledkom.

- Zamenjava iskanih bitov v vhodni binarni datoteki (t. i. find + replace all)

 

Vhod/izhod konzolne aplikacije (preko argumentov)

dn1 <vhodna datoteka> <opcija> <podatek1> <podatek2>

kjer:

<opcija>:
f - operacija iskanja bitov iz <podatek1>
fr - operacija zamenjava bitov iz <podatek1> z biti iz <podatek2>
<podatek1> in <podatek2> - zaporedje bitov
<vhodna datoteka> - pot do poljubne datoteke, ki jo odprete v binarnem načinu.
Primer uporabe:

dn1 test.bin f 0110100001100101011011000110110001101111

dn1 test.bin fr 0000000 1111

 