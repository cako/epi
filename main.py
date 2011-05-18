#!/usr/bin/python
# -*- coding: UTF-8 -*-
""" Main. Runs a terminal version of the program. """

import epi_classes

run = 0
TMain = epi_classes.TerminalMain()
while (run == 0):
    run = TMain.run()
