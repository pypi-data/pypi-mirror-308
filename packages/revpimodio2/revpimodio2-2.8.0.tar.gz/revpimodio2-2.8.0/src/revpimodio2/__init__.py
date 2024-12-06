# -*- coding: utf-8 -*-
"""
Stellt alle Klassen fuer den RevolutionPi zur Verfuegung.

Webpage: https://revpimodio.org/

Stellt Klassen fuer die einfache Verwendung des Revolution Pis der
KUNBUS GmbH (https://revolution.kunbus.de/) zur Verfuegung. Alle I/Os werden
aus der piCtory Konfiguration eingelesen und mit deren Namen direkt zugreifbar
gemacht. Fuer Gateways sind eigene IOs ueber mehrere Bytes konfigurierbar
Mit den definierten Namen greift man direkt auf die gewuenschten Daten zu.
Auf alle IOs kann der Benutzer Funktionen als Events registrieren. Diese
fuehrt das Modul bei Datenaenderung aus.
"""
__all__ = [
    "IOEvent",
    "RevPiModIO",
    "RevPiModIODriver",
    "RevPiModIOSelected",
    "run_plc",
    "RevPiNetIO",
    "RevPiNetIODriver",
    "RevPiNetIOSelected",
    "run_net_plc",
    "Cycletools",
    "EventCallback",
    "ProductType",
    "DeviceType",
    "AIO",
    "COMPACT",
    "DI",
    "DO",
    "DIO",
    "FLAT",
    "MIO",
]
__author__ = "Sven Sager <akira@revpimodio.org>"
__copyright__ = "Copyright (C) 2023 Sven Sager"
__license__ = "LGPLv2"

from .__about__ import __version__
from ._internal import *
from .helper import Cycletools, EventCallback
from .io import IOEvent
from .modio import RevPiModIO, RevPiModIODriver, RevPiModIOSelected, run_plc
from .netio import RevPiNetIO, RevPiNetIODriver, RevPiNetIOSelected, run_net_plc
from .pictory import ProductType, DeviceType, AIO, COMPACT, DI, DO, DIO, FLAT, MIO
