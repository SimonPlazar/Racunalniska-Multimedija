# Vaja 2

V poljubnem programskem jeziku izdelajte konzolno aplikacijo, ki bo omogočila odpiranje poljubnih sivinskih BMP slik ter kompresijo in dekompresijo le-teh z algoritmom temelječim na diskretni Haarovi transformaciji.

 

Uporabniku naj bo omogočeno sledeče:

Nastavitev pragu stiskanja.
Shranjevanje kompresirane slike in izvedba dekompresije nad prebrano kompresirano sliko.
Hramba dekompresirane slike na disk v izvornem formatu.
Za kodiranje entropije lahko uporabite poljubno knjižico ali lastno implementacijo aritmetičnega kodirnika.

 

Vhod/izhod konzolne aplikacije (preko argumentov)

dn2 <vhodna datoteka> <opcija> <izhodna datoteka> <thr>

kjer:

<opcija>:
c - kompresija
d - dekompresija
<vhodna datoteka> - pot do poljubne datoteke, ki vsebuje sliko
<izhodna datoteka> - pot do izhodne binarne datoteke (po kompresiji) ali slike (po dekompresiji)
<thr> - prag pri kompresiji
  


Poročilo

Poleg vaje pripravite in oddajte tudi poročilo (1 do 2 strani) v formatu PDF. Uporabite 10 sivinskih BMP slik in poročajte naslednje ugotovitve:

Kompresijsko razmerje (graf ali tabela)
Prikažite (graf ali tabela) izračun PSNR metrike, Shannonove entropije, Blokovnosti med originalno in dekompresiroano sliko. Pri tem testirajte s pragom stiskanja thr={0, 25, 50, 100}