# can-diagnostics-simulatornew
# UDS Diagnostics Simulator

This project simulates basic UDS diagnostic communication similar to the DST/DMT testing I performed at Bosch.
It demonstrates how diagnostic requests (0x10, 0x19, 0x14) are processed and how ECUs respond with positive or
negative responses.

## Features
- Diagnostic Session Control (0x10)
- Read DTC Information (0x19)
- Clear DTC Information (0x14)
- ECU response simulation
- Simple DTC database

## How to Run
python uds_simulator.py

