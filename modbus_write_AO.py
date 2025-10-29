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

# --- Parameter ---
Kp = 1.0          # Proportionalfaktor
Ki = 0.5          # Integralfaktor
setpoint = 10.0   # Sollwert
dt = 0.1          # Abtastzeit (10 Hz)

def set_drive(frequency):

    voltage = frequency * 0.2  # 0..10V bei 50Hz
    # Scale to 0..32767 (16-bit signed positive range used by device)
    int_value = int(round((voltage / 10.0) * 32767))
    # Clamp to valid 16-bit unsigned range just in case
    int_value = max(0, min(65535, int_value))
    c.write_single_register(0x0800, int_value)

def pi_controller(setpoint, measured_value, Kp, Ki, integral, dt):
    error = setpoint - measured_value
    integral += error * dt
    output = Kp * error + Ki * integral
    return output, integral

integral = 0.0

state = "run"
frequency_drive = 30  # Hz

# Verbindung initialisieren
c = ModbusClient(host="192.168.1.4", port=502, unit_id=1, auto_open=True)

while state == "run":

    

    #output, integral = pi_controller(setpoint, measured_value, Kp, Ki, integral, dt)

    set_drive(20)
    #if frequency_drive >= 50:
    #    state = "stop"
    voltage = c.read_input_registers(0x0001, 2)
    print((voltage[1]+voltage[0]*1/(2**16))/16)
    time.sleep(0.5)

if state == "stop":
    c.close()