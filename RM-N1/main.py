import argparse
from collections import defaultdict


def kompresija(vhodni_niz, tabela_verjetnosti, kumulativna_frekvenca, stevilo_bitov=8):
    # Inicializacija globalnega intervala
    spodnja_meja = 0
    zgornja_meja = (2 ** (stevilo_bitov - 1)) - 1

    prva_cetrtina = (zgornja_meja + 1) // 4
    druga_cetrtina = (zgornja_meja + 1) // 2
    tretja_cetrtina = prva_cetrtina * 3

    e3_counter = 0
    izhod = []

    trenutni_biti = 0  # To keep track of the current byte being built
    stevilo_zapolnjenih_bitov = 0  # Counts how many bits have been added to trenutni_biti

    # Funkcija za dodajanje bitov v izhod (as a byte stream)
    def dodaj_bit(bit):
        nonlocal trenutni_biti, stevilo_zapolnjenih_bitov
        trenutni_biti = (trenutni_biti << 1) | bit
        stevilo_zapolnjenih_bitov += 1

        if stevilo_zapolnjenih_bitov == 8:
            izhod.append(trenutni_biti)  # Append full byte
            trenutni_biti = 0
            stevilo_zapolnjenih_bitov = 0

    # Funkcija za preslikave E1, E2 in E3
    def preslikava_e1():
        nonlocal spodnja_meja, zgornja_meja, e3_counter
        dodaj_bit(0)
        spodnja_meja *= 2
        zgornja_meja = 2 * zgornja_meja + 1
        while e3_counter > 0:
            dodaj_bit(1)
            e3_counter -= 1

    def preslikava_e2():
        nonlocal spodnja_meja, zgornja_meja, e3_counter
        dodaj_bit(1)
        spodnja_meja = 2 * (spodnja_meja - druga_cetrtina)
        zgornja_meja = 2 * (zgornja_meja - druga_cetrtina) + 1
        while e3_counter > 0:
            dodaj_bit(0)
            e3_counter -= 1

    def preslikava_e3():
        nonlocal spodnja_meja, zgornja_meja, e3_counter
        spodnja_meja = 2 * (spodnja_meja - prva_cetrtina)
        zgornja_meja = 2 * (zgornja_meja - prva_cetrtina) + 1
        e3_counter += 1

    # Kodiranje posameznega byte-a
    for znak in vhodni_niz:
        # Dobimo verjetnostni interval za byte
        sp_znak, zg_znak = tabela_verjetnosti[znak]

        # Izračun koraka
        korak = (zgornja_meja - spodnja_meja + 1) // kumulativna_frekvenca

        # Posodobimo meje glede na interval byte-a
        zgornja_meja = spodnja_meja + korak * zg_znak - 1
        spodnja_meja = spodnja_meja + korak * sp_znak

        # Preslikave E1, E2, E3
        while True:
            if zgornja_meja < druga_cetrtina:
                preslikava_e1()
            elif spodnja_meja >= druga_cetrtina:
                preslikava_e2()
            elif (spodnja_meja >= prva_cetrtina) and (zgornja_meja < tretja_cetrtina):
                preslikava_e3()
            else:
                break

    # Končna vrednost
    if spodnja_meja < prva_cetrtina:
        dodaj_bit(0)
        dodaj_bit(1)
        while e3_counter > 0:
            dodaj_bit(1)
            e3_counter -= 1
    else:
        dodaj_bit(1)
        dodaj_bit(0)
        while e3_counter > 0:
            dodaj_bit(0)
            e3_counter -= 1

    # If there are remaining bits in the current byte, pad with zeros and add to the output
    if stevilo_zapolnjenih_bitov > 0:
        trenutni_biti <<= (8 - stevilo_zapolnjenih_bitov)  # Shift remaining bits to form a full byte
        izhod.append(trenutni_biti)

    return bytearray(izhod)  # Return as a byte array


def dekompresija(encoded_bytes, tabela_verjetnosti, kumulativna_frekvenca, stevilo_bitov=8):
    # Convert the byte stream into a bit stream
    encoded_bits = ''.join(f'{byte:08b}' for byte in encoded_bytes)  # Convert bytes to binary string

    # Inicializacija globalnega intervala
    spodnja_meja = 0
    zgornja_meja = (2 ** (stevilo_bitov - 1)) - 1

    prva_cetrtina = (zgornja_meja + 1) // 4
    druga_cetrtina = (zgornja_meja + 1) // 2
    tretja_cetrtina = prva_cetrtina * 3

    polje = int(encoded_bits[:stevilo_bitov - 1], 2)  # Inicialno polje z začetnimi biti
    trenutni_bit_index = stevilo_bitov - 1  # Kazalec na trenutno pozicijo v vhodnem nizu bitov

    # Funkcija za pridobitev naslednjega bita
    def naslednji_bit():
        nonlocal trenutni_bit_index
        if trenutni_bit_index < len(encoded_bits):
            bit = int(encoded_bits[trenutni_bit_index])
            trenutni_bit_index += 1
            return bit
        return 0  # Ko zmanjka bitov, vrnemo 0

    # Funkcija za iskanje simbola na podlagi vrednosti
    def najdi_simbol(vrednost):
        for znak, (sp_meja, zg_meja) in tabela_verjetnosti.items():
            if sp_meja <= vrednost < zg_meja:
                return znak
        return None

    # Dekodiranje simbola
    output = bytearray()
    while 1:
        # Izračun koraka
        korak = (zgornja_meja - spodnja_meja + 1) // kumulativna_frekvenca

        # Izračun vrednosti
        vrednost = (polje - spodnja_meja) // korak

        # Najdemo simbol v tabeli
        simbol = najdi_simbol(vrednost)
        if simbol is None:
            break
        output.append(simbol)  # Append the byte (symbol) to the output

        # Posodobimo meje za naslednji simbol
        sp_meja, zg_meja = tabela_verjetnosti[simbol]
        zgornja_meja = spodnja_meja + korak * zg_meja - 1
        spodnja_meja = spodnja_meja + korak * sp_meja

        # Preslikave E1, E2 in E3
        while True:
            if zgornja_meja < druga_cetrtina:
                # E1 preslikava
                spodnja_meja = spodnja_meja * 2
                zgornja_meja = (2 * zgornja_meja) + 1
                polje = 2 * polje + naslednji_bit()
            elif spodnja_meja >= druga_cetrtina:
                # E2 preslikava
                spodnja_meja = 2 * (spodnja_meja - druga_cetrtina)
                zgornja_meja = 2 * (zgornja_meja - druga_cetrtina) + 1
                polje = 2 * (polje - druga_cetrtina) + naslednji_bit()
            elif (spodnja_meja >= prva_cetrtina) and (zgornja_meja < tretja_cetrtina):
                # E3 preslikava
                spodnja_meja = 2 * (spodnja_meja - prva_cetrtina)
                zgornja_meja = 2 * (zgornja_meja - prva_cetrtina) + 1
                polje = 2 * (polje - prva_cetrtina) + naslednji_bit()
            else:
                break

    return output  # Return bytearray output


def compress_file(vhodna_datoteka, izhodna_datoteka, stevilo_bitov):
    # Ustvarimo slovar za štetje frekvenc byte-ov
    frekvence = defaultdict(int)

    vhodni_niz = bytearray()

    # Preberemo datoteko byte po byte
    with open(vhodna_datoteka, 'rb') as vhodna:
        while (znak := vhodna.read(1)):  # Read one byte at a time
            frekvence[znak[0]] += 1  # Treat 'znak' as a byte (int)
            vhodni_niz.append(znak[0])  # Append the byte to the input bytearray

    if len(frekvence) > 2 ** stevilo_bitov:
        print(f"Preveč različnih znakov za {stevilo_bitov} bitov.")
        return

    # Izračunamo kumulativne frekvence in ustvarimo verjetnostno tabelo
    tabela_verjetnosti = {}
    skupna_frekvenca = sum(frekvence.values())
    kumulativna_frekvenca = 0

    for znak, frekvenca in frekvence.items():
        # Spodnja meja in zgornja meja
        sp_meja = kumulativna_frekvenca
        zg_meja = kumulativna_frekvenca + frekvenca
        tabela_verjetnosti[znak] = (sp_meja, zg_meja)
        kumulativna_frekvenca += frekvenca

    assert kumulativna_frekvenca == skupna_frekvenca

    # Izpišemo tabelo verjetnosti (optional)
    # print("Tabela verjetnosti:")
    # print(f"{'Byte':<4} {'Frekvenca':<10} {'spMeja':<8} {'zgMeja':<8}")
    # for znak, (sp_meja, zg_meja) in tabela_verjetnosti.items():
    #     print(f"{znak:<4} {frekvence[znak]:<10} {sp_meja:<8} {zg_meja:<8}")

    # Call the kompresija function with byte data
    output = kompresija(vhodni_niz, tabela_verjetnosti, kumulativna_frekvenca, stevilo_bitov=stevilo_bitov)

    # Na koncu lahko shranite izhod v datoteko
    with open(izhodna_datoteka, 'wb') as izhodna:
        # Write the bit depth and frequency table
        izhodna.write(stevilo_bitov.to_bytes(1, 'big'))  # Write bit depth as one byte
        izhodna.write(len(tabela_verjetnosti).to_bytes(stevilo_bitov // 8, 'big'))  # Write number of unique bytes

        # Write the frequency table (byte value and frequency)
        for znak, (sp_meja, zg_meja) in tabela_verjetnosti.items():
            izhodna.write(znak.to_bytes(1, 'big'))  # Write the byte value
            izhodna.write(frekvence[znak].to_bytes(stevilo_bitov // 8, 'big'))  # Write frequency for that byte

        # Write the compressed output bytes
        izhodna.write(output)


def decompress_file(vhodna_datoteka, izhodna_datoteka):
    with open(vhodna_datoteka, 'rb') as vhodna:
        # Preberemo število bitov (bit depth)
        stevilo_bitov = int.from_bytes(vhodna.read(1), 'big')
        stevilo_bytov = stevilo_bitov // 8

        # Preberemo število različnih znakov (by the size of the frequency table)
        st_znakov = int.from_bytes(vhodna.read(stevilo_bytov), 'big')

        kumulativna_frekvenca = 0
        tabela_verjetnosti = {}

        # Preberemo tabelo verjetnosti
        for _ in range(st_znakov):
            znak = int.from_bytes(vhodna.read(1), 'big')  # Preberemo byte
            frekvenca = int.from_bytes(vhodna.read(stevilo_bytov), 'big')  # Preberemo frekvenco
            tabela_verjetnosti[znak] = (kumulativna_frekvenca, kumulativna_frekvenca + frekvenca)
            kumulativna_frekvenca += frekvenca

        # Preostanek datoteke so stisnjeni biti
        vhodni_biti = vhodna.read()  # Preberemo preostale byte, ki vsebujejo kodirane bite

    # Dekodiramo kodirane bite in dobimo izhodne byte
    output = dekompresija(vhodni_biti, tabela_verjetnosti, kumulativna_frekvenca, stevilo_bitov=stevilo_bitov)

    # Shranimo dekompresiran rezultat kot bytearray
    with open(izhodna_datoteka, 'wb') as izhodna:
        izhodna.write(bytearray(output))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Kompresija ali dekompresija datotek.")
    parser.add_argument('operacija', choices=['c', 'd'], help="Izberite 'c' za kompresijo ali 'd' za dekompresijo.")
    parser.add_argument('vhodna_datoteka', help="Pot do vhodne datoteke.")
    parser.add_argument('izhodna_datoteka', help="Pot do izhodne datoteke.")

    args = parser.parse_args()

    stevilo_bitov = 32

    if args.operacija == 'c':
        compress_file(args.vhodna_datoteka, args.izhodna_datoteka, stevilo_bitov)
    elif args.operacija == 'd':
        decompress_file(args.vhodna_datoteka, args.izhodna_datoteka)
