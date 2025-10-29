# -*- coding: utf-8 -*-
"""
Erstellt: 28.10.2025
Christian Oxé, FHNW
Steuert zwei Umrichter und regelt das Drehmoment der Lastmaschine.
"""
# Imortiert pyModbusTCP und Time Libraries
from pyModbusTCP.client import ModbusClient
import sys
import logging
from math import sqrt
import time


# Verbindung initialisieren
c = ModbusClient(host="192.168.1.4", port=502, unit_id=1, auto_open=True)

frequency = 25.0  # Hz

voltage = frequency * 0.2  # 0..10V bei 50Hz
# Scale to 0..32767 (16-bit signed positive range used by device)
int_value = int(round((voltage / 10.0) * 32767))
# Clamp to valid 16-bit unsigned range just in case
int_value = max(0, min(65535, int_value))
c.write_single_register(0x0800, int_value)

voltage = c.read_input_registers(0x0001, 2)
print((voltage[1]+voltage[0]*1/(2**16))/16)
time.sleep(0.5)

c.close()