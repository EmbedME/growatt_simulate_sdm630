# Simulate SDM630 for testing export limitation on Growatt MIC 600TL-X

This python script simulates a SDM630 energy meter, it provides the modbus register 30053 (total system power in Watt) which the Growatt MIC 600TL-X requests over RS485 when export limitation is activated.  
Usage:
```
./growatt_simulate_sdm630.py SERIALPORT TOTAL_SYSTEM_POWER_IN_WATT
```

## Bug in MIC 600TL-X firmware: Export limitation stopps on higher (>~2kW) meter values

### Problem:
The export limitation works in principle, but when the total power (reported by the meter) goes above ~2kW, the inverter goes down to ~6W.
Observed with Firmware: GH1.0

Other users also report this problem:
https://www.photovoltaikforum.com/thread/168815-growatt-1500tlx-durch-smartmeter-steuern/?postID=2702847#post2702847

### These steps show the problem:
1. Turn on export limit with 100% on MIC 600TL-X (menu -> advanced setting)
2. Wire RS485 (signals A and B, 120 Ohm termination an both ends) and connect RS485 interface to computer
3. Simulate power export of 300W: `./growatt_simulate_sdm630.py /dev/ttyUSB0 300`
=> OK: regulation works
4. Simulate power export of 2300W: `./growatt_simulate_sdm630.py /dev/ttyUSB0 2300`
=> **FAIL: inverter power goes down to ~6W**

I've contacted the Growatt support. If a solution is found, I will report here.
