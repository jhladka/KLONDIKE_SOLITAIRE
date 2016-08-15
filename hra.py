#!/usr//bin/python
# -*- coding: utf-8 -*-

import klondike

hra = klondike.vyrob_hru()
klondike.vypis_hru(hra)
while not klondike.hrac_vyhral(hra):
    tah = klondike.nacitaj_tah()
    try:
        info = klondike.priprav_tah(hra, tah)
    except ValueError as e:
        print(e)
    else:
        klondike.urob_tah(hra,info)
        klondike.vypis_hru(hra)
