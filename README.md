# EDLC.tester
# Supercapacitor Testing and ESR Measurement

## Project Overview
This project involves testing various supercapacitors to gather constant voltage readings, calculate total Equivalent Series Resistance (ESR), and determine the final capacitance values. The testing procedure utilizes SCPI commands sent via Python to control two instruments: a Chroma electronic load and a DAQ (Data Acquisition) system. These instruments allow us to measure voltage, control the charge and discharge cycles of the supercapacitors, and compute key metrics for analysis.

## Key Features
- **Charge and Discharge Cycles**: The system charges the supercapacitors at constant current and switches to constant voltage once the rated voltage is reached. After charging, the system discharges at constant current.
- **Voltage Monitoring**: Voltage measurements are taken throughout the charge and discharge cycles, providing real-time monitoring of the capacitor's performance.
- **ESR Calculation**: The system calculates the ESR during both charging and discharging cycles to give insights into the supercapacitor’s internal losses.
- **Capacitance Calculation**: The final capacitance is calculated based on the gathered data, allowing comparison between different supercapacitors.
  
## Instruments Used
- **Chroma Electronic Load**: Used for controlling the charge and discharge cycles.
- **DAQ (Data Acquisition) System**: Used for voltage measurements across multiple channels.
  
## Dependencies
- Python 3.x
- [pyvisa](https://pyvisa.readthedocs.io/en/stable/) – Library for communication with instruments using VISA
- Chroma Electronic Load
- DAQ Instrument
