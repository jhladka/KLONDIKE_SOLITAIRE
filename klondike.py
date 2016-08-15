# -*- coding: utf-8 -*-
import random


def popis_farby(farba):
    farby = {'Sr': 'S',
             'Ka': 'K',
             'Pi': 'P',
             'Kr': '+',
             }
    return farby[farba]


def popis_hodnoty(hodnota):
    hodnoty = {1: 'A',
               2: '2',
               3: '3',
               4: '4',
               5: '5',
               6: '6',
               7: '7',
               8: '8',
               9: '9',
               10: 'X',
               11: 'J',
               12: 'Q',
               13: 'K'
               }
    return hodnoty[hodnota]


def otoc_kartu(karta, nove_otocenie):
    hodnota, farba, licom_hore = karta
    return hodnota, farba, nove_otocenie


def popis_karty(karta):
    licom_hore = karta[2]  # !/usr/bin/python
    if licom_hore == True:
        hodnota = karta[0]
        farba = karta[1]
        if farba in ('Sr', 'Ka'):
            # red: hearts or diamonds
            return '[%s %s]' % (popis_hodnoty(hodnota), popis_farby(farba))
        else:
            # black: spades or clubs
            return '[%s%s ]' % (popis_hodnoty(hodnota), popis_farby(farba))
    else:
        return '[???]'


def popis_balicka(balicek):
    if len(balicek) == 0:
        return '[   ]'
    else:
        return popis_karty(balicek[-1])


def vyrob_hru():
    # vyrobi a zamiesa karty
    karty = []
    for i in xrange(1, 14):
        for j in ('Sr', 'Ka', 'Pi', 'Kr'):
            karty.append((i, j, False))
    random.shuffle(karty)
    # naplni stlpceky kartami
    stlpceky = []
    for i in xrange(7):
        balicek = []
        for j in xrange(i):
            balicek.append(karty.pop())
        balicek.append(otoc_kartu(karty.pop(), True))
        stlpceky.append(balicek)
    # odlozi zvysne karty do balicka
    balicky = [karty, []]
    # a este vytvori hromadky na skladanie kariet
    hromadky = [[], [], [], []]
    hra = [balicky, hromadky, stlpceky]
    return hra


def vypis_hru(hra):
    vypis = ''
    # 1.riadok
    for ozn in ('UV WXYZ'):
        vypis += '  ' + ozn + '   '
    vypis += '\n'
    # 2. a 3.riadok
    for balicek in hra[0]:
        vypis += popis_balicka(balicek) + ' '
    vypis += '      '
    for balicek in hra[1]:
        vypis += popis_balicka(balicek) + ' '
    vypis += '\n\n'
    # 4.riadok
    for ozn in ('ABCDEFG'):
        vypis += '  ' + ozn + '   '
    vypis += '\n'
    # 5. az ??.riadok
    MAX = [len(stlpec) for stlpec in hra[2]]
    for r in range(max(MAX)):
        riadok = ''
        for s in range(7):
            if r < MAX[s]:
                riadok += popis_karty(hra[2][s][r]) + ' '
            else:
                riadok += '      '
        vypis += riadok + '\n'
    print vypis


def hrac_vyhral(hra):
    vyhral = True
    for hromadka in hra[1]:
        if len(hromadka) <> 13:
            vyhral = False
    return vyhral


MOZNOSTI_Z = 'ABCDEFGV'
MOZNOSTI_NA = 'ABCDEFGWXYZ'
NAPOVEDA = """
Příkazy:
? - Vypíše tuto nápovědu.
U - Otočí kartu balíčku (z U do V).
    Nebo doplní balíček U, pokud je prázdný.
EC - Přemístí karty z E na C.
     Za E dosaď odkud karty vzít: A-G nebo V.
     Za C dosaď kam chceš karty dát: A-G nebo W-Z.
E2G - Přemístí 2 karty z E na C
      Za E dosaď odkud kartu vzít: A-G nebo V.
      Za 2 dosaď počet karet.
      Za C dosaď kam chceš kartu dát: A-G nebo W-Z.
Ctrl+C - Ukončí hru
"""


def nacitaj_tah():
    """
    Zeptá se uživatele, co dělat

    Stará se o výpis nápovědy.

    Může vrátit buď řetězec 'U' ("lízni z balíčku"), nebo trojici
    (z, pocet, na), kde:
        - `z` je číslo místa, ze kterého karty vezmou (A-G: 0-6; V: 7)
        - `pocet` je počet karet, které se přemisťují
        - `na` je číslo místa, kam se karty mají dát (A-G: 0-6, W-Z: 7-10)

    Zadá-li uživatel špatný vstup, zeptá se znova.
    """
    while True:
        tah = raw_input('Zadaj ťah: ')
        tah = tah.upper()
        if tah[0] == '?':
            print NAPOVEDA
        elif tah == 'U':
            return 'U'
        elif len(tah) < 2:
            print 'Nerozumiem ťahu!'
        elif tah[0] in MOZNOSTI_Z and tah[-1] in MOZNOSTI_NA:
            if len(tah) == 2:
                pocet = 1
            else:
                try:
                    pocet = int(tah[1:-1])
                except ValueError:
                    print ('"{}" nie je číslo!'.format(tah[1:-1]))
                    continue
            return (MOZNOSTI_Z.index(tah[0]), pocet, MOZNOSTI_NA.index(tah[-1]))
        else:
            print 'Nerozumiem tahu!'
                
                
def priprav_tah(hra, tah):
    """
    Zkontroluje, že je tah podle pravidel

    Jako argument bere hru, a tah získaný z funkce `nacitaj_tah`.

    Vrací buď řetězec 'U' ("lízni z balíčku"), nebo trojici
    (zdrojovy_balicek, pocet, cilovy_balicek), kde `*_balicek` jsou přímo
    seznamy, ze kterých/na které se budou karty přemisťovat, a `pocet` je 
    počet karet k přemístění.

    Není-li tah podle pravidel, funkce vyvolá výjimku `ValueError` s nějakou
    rozumnou chybovou hláškou.
    """
    Z = 'ABCDEFGV'
    # tahy z balicka resp. doplnenie balicka
    if tah == 'U':
        if len(hra[0][0]) == 0 and len(hra[0][1]) == 0:
            raise ValueError('V balíčku U už nie sú žiadne karty!')
        else:
            return 'U'
    # presuvanie kariet
    else:
        z, pocet, na = tah
        balicky, hromadky, stlpceky = hra
        # presuvanie karty/kariet zo stlpceka
        if z < 7:
            z_balicka = stlpceky[z]
            if pocet > len(z_balicka):
                raise ValueError('Na to nie je v {} dosť kariet!'.format(Z[z]))
            for i in range(pocet):
                if z_balicka[-i-1][2] == False:
                    raise ValueError('Nemôžeš presúvať karty, ktoré sú rubom hore!')
        # potiahnutie karty z balicka V
        else:
            if pocet > 1:
                raise ValueError('Z balíčka V sa nedá brať viac kariet naraz!')
            z_balicka = balicky[1]
        # presunutie karty/kariet do stlpceka
        if na < 7:
            na_balicek = stlpceky[na]
            if len(na_balicek) == 0:
                if z_balicka[-pocet][0] != 13:
                    raise ValueError('Do prázdneho stĺpca môže ísť len kráľ!')
            # skontroluje postupku
            else:
                if na_balicek[-1][0] != z_balicka[-pocet][0] + 1:
                    raise ValueError('Musíš robiť zostupné postupky!')
                if [popis_karty(na_balicek[-1])[2], popis_karty(z_balicka[-pocet])[2]].count(' ') != 1:
                    raise ValueError('Musíš striedať farby!')
        # presunutie karty na hromadku
        else:
            na_balicek = hromadky[na - 7]
            if pocet > 1:
                raise ValueError('Na hromádku sa nedá dať viac kariet naraz!')
            if len(na_balicek) == 0:
                if z_balicka[-1][0] != 1:
                    raise ValueError('Na prázdnu hromádku môže ísť len eso!')
            else:
                if na_balicek[-1][1] != z_balicka[-1][1]:
                    raise ValueError('Hromádka musí mať jednu farbu!')
                if na_balicek[-1][0] + 1 != z_balicka[-1][0]:
                    raise ValueError('Na hromádku musíš skladať karty postupne od najnižších!')
        return (z_balicka, pocet, na_balicek)


def urob_tah(hra, info_o_tahu):
    # otocenie karty z balicku
    if info_o_tahu == 'U':
        balicekU = hra[0][0]
        balicekV = hra[0][1]
        if len(balicekU) > 0:
            balicekV.append(otoc_kartu(balicekU.pop(), True))
        # ak je doberaci balicek prazdny, presunie a otoci zahodene karty
        else:
            for i in range(len(balicekV)):
                balicekU.append(otoc_kartu(balicekV.pop(),False))
    # presunie kartu/y
    else:
        z_balicka, pocet, na_balicek = info_o_tahu
        na_balicek.extend(z_balicka[-pocet:])
        del z_balicka[-pocet:]
        if len(z_balicka) > 0:
            vrchna_karta = z_balicka[-1]
            if vrchna_karta[2] == False:
                del z_balicka[-1]
                z_balicka.append(otoc_kartu(vrchna_karta, True))          
    return hra
