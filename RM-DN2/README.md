# Domača naloga 2

V poljubnem programskem jeziku implementirajte aplikacijo za skrivanje informacij v frekvenčnem prostoru poljubnih sivinskih BMP slik na podlagi steganografskega algoritma F5.

 

Algoritem

Skrivanje sporočila

1. Tekstovno sporočilo, ki ga boste skrili najprej binarizirajte. Na začetek binariziranega sporočila dodajte 4 zloge, kjer s celim številom (uint) poveste velikost sporočila v bitih.

2. Sivinsko sliko razdelite na 8x8 bloke pikslov.

3. Posamezni blok pretvorite v frekvenčni prostor na podlagi Haarove transformacije.

4. Izvedite kvantizacijo frekvenčnega prostora v bloku, kjer najprej serializirajte 64 koeficientov z algoritmom cik-cak, nato pa postavite zadnjih N koeficentov na 0 (uporabnik določi N). Koeficiente zaokrožite v cela števila (integer).

5. Izberite naključni blok (nad katerim še niste uporabili algoritma F5) ter nad (64 - N) koeficienti bloka izvedite algoritem F5:

Izberite M naključnih unikatnih trojic koeficientov srednjih frekvenc (indeksi od 4 do 32, v primeru večjega N se ta razpon zmanjša!). Trojice med sabo nimajo prekrivanja.
Vsako trojico določajo koeficienti AC1, AC2 in AC3, kjer so korespodenčni LSB (angl. least significant bit) biti danih koeficentov definirani kot C1 = LSB(AC1), C2 = LSB(AC2) in C3 = LSB(AC3).
Za vsako trojico (C1, C2, C3) vzamite 2 bita binariziranega sporočila, definirana kot x1 in x2 ter izvedite naslednje operacije za skrivanje x1 in x2:
          

6. Koeficiente blokov shranite v binarno datoteko.

 

Ekstrakcija sporočila

Inverzni postopek, kjer naredite ekstrakcijo sporočila preden pretvorite koeficiente bloka nazaj s pomočjo Haarove transformacije. Na koncu prikažite sporočilo in shranite dekompresirano sliko.

Seme naključnega generatorja števil je definirano kot M*N (pazite, da je pri ekstrakciji - inverzu enako seme!).

  
 
Vhod/izhod konzolne aplikacije (preko argumentov)

vaja3 <vhodna slika> <opcija> <vhodno/izhodno sporočilo> <N> <M>

kjer:

<vhodna datoteka> - pot do poljubne slike.
<opcija>:
h - skrivanje sporočila
e - ekstrakcija sporočila
<vhodno/izhodno sporočilo> - pot do vhodnega/izhodnega tekstovnega sporočila.
<N> - prag pri kompresiji
<M> - število unikatnih množic trojic koeficientov, ki se uporabijo v F5 steganografiji.
 

Poročilo

Poleg domače naloge pripravite in oddajte tudi poročilo (1 do 2 strani) v formatu PDF. Uporabite 2 različni sivinski BMP sliki in 2 različna sporočila. Poročajte naslednje ugotovitve:

Prikažite (graf ali tabela) izračun PSNR metrike, Shannonove entropije, Blokovnosti med original in modificirano sliko (po skrivanju). Pri tem testirajte s kombinacijo N={1, 20, 40} ter M={1, 3, 5}
Blokovnost izračunate kot:
               , kjer je g slika ločljivosti MxN.

Prikažite dva histograma za intenziteto vseh pikslov pred in po modifikacijo pri N=20 in M=3. Smiselno izberite št. košev v histogramu.
