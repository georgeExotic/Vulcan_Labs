EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:HP45 controller parts
LIBS:HP45 breakout board SA3-cache
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L HP45_connector Con1
U 1 1 5AB3E7C4
P 3200 3900
F 0 "Con1" H 3550 4000 60  0000 C CNN
F 1 "HP45_connector" H 3000 4000 60  0000 C CNN
F 2 "Electronics:HP45_SMD_connector" H 3200 3900 60  0001 C CNN
F 3 "" H 3200 3900 60  0001 C CNN
	1    3200 3900
	1    0    0    -1  
$EndComp
$Comp
L CONN_02X10 J1
U 1 1 5AB3E92B
P 2100 2100
F 0 "J1" H 2100 2650 50  0000 C CNN
F 1 "CONN_02X10" V 2100 2100 50  0000 C CNN
F 2 "Socket_Strips:Socket_Strip_Straight_2x10_Pitch2.54mm" H 2100 900 50  0001 C CNN
F 3 "" H 2100 900 50  0001 C CNN
	1    2100 2100
	-1   0    0    -1  
$EndComp
$Comp
L CONN_02X10 J2
U 1 1 5AB3E956
P 4100 2100
F 0 "J2" H 4100 2650 50  0000 C CNN
F 1 "CONN_02X10" V 4100 2100 50  0000 C CNN
F 2 "Socket_Strips:Socket_Strip_Straight_2x10_Pitch2.54mm" H 4100 900 50  0001 C CNN
F 3 "" H 4100 900 50  0001 C CNN
	1    4100 2100
	-1   0    0    -1  
$EndComp
Text Label 2200 4000 0    60   ~ 0
HGND
Wire Wire Line
	2200 5600 2600 5600
Wire Wire Line
	2600 4800 2200 4800
Wire Wire Line
	2200 4400 2600 4400
Wire Wire Line
	2600 4000 2200 4000
Wire Wire Line
	2200 6300 2600 6300
Wire Wire Line
	2600 6100 2200 6100
Wire Wire Line
	2200 6000 2600 6000
Text Label 4200 6500 2    60   ~ 0
HGND
Wire Wire Line
	4200 6500 3800 6500
Text Label 4200 6100 2    60   ~ 0
HGND
Text Label 4200 5700 2    60   ~ 0
HGND
Text Label 4200 4900 2    60   ~ 0
HGND
Text Label 4200 4500 2    60   ~ 0
HGND
Text Label 4200 4400 2    60   ~ 0
HGND
Wire Wire Line
	4200 4400 3800 4400
Wire Wire Line
	3800 4500 4200 4500
Wire Wire Line
	4200 4900 3800 4900
Wire Wire Line
	4200 5700 3800 5700
Wire Wire Line
	3800 6100 4200 6100
Text Label 4200 4200 2    60   ~ 0
HGND
Wire Wire Line
	4200 4200 3800 4200
Text Label 4200 5600 2    60   ~ 0
P1
Text Label 2200 5900 0    60   ~ 0
P2
Text Label 2200 5500 0    60   ~ 0
P0
Wire Wire Line
	4200 5600 3800 5600
Wire Wire Line
	2200 5500 2600 5500
Wire Wire Line
	2200 5900 2600 5900
Text Label 2200 6200 0    60   ~ 0
P4
Wire Wire Line
	2200 6200 2600 6200
Text Label 2200 6400 0    60   ~ 0
P6
Wire Wire Line
	2200 6400 2600 6400
Text Label 2200 4900 0    60   ~ 0
P12
Wire Wire Line
	2200 4900 2600 4900
Text Label 2200 4500 0    60   ~ 0
P10
Wire Wire Line
	2200 4500 2600 4500
Text Label 2200 4100 0    60   ~ 0
P8
Wire Wire Line
	2200 4100 2600 4100
Text Label 4200 6400 2    60   ~ 0
P5
Text Label 4200 6000 2    60   ~ 0
P3
Text Label 4200 5000 2    60   ~ 0
P13
Text Label 4200 4600 2    60   ~ 0
P11
Text Label 4200 4300 2    60   ~ 0
P9
Text Label 4200 4100 2    60   ~ 0
P7
Wire Wire Line
	4200 6400 3800 6400
Wire Wire Line
	4200 6000 3800 6000
Wire Wire Line
	4200 5000 3800 5000
Wire Wire Line
	4200 4600 3800 4600
Wire Wire Line
	4200 4300 3800 4300
Wire Wire Line
	4200 4100 3800 4100
Text Label 4200 4000 2    60   ~ 0
A13
Wire Wire Line
	4200 4000 3800 4000
Text Label 4200 4700 2    60   ~ 0
A15
Text Label 4200 4800 2    60   ~ 0
A17
Text Label 4200 5100 2    60   ~ 0
A19
Wire Wire Line
	3800 5100 4200 5100
Wire Wire Line
	4200 4700 3800 4700
Wire Wire Line
	3800 4800 4200 4800
Text Label 4200 5300 2    60   ~ 0
A21
Text Label 4200 5400 2    60   ~ 0
A20
Text Label 4200 5500 2    60   ~ 0
A18
Text Label 4200 5800 2    60   ~ 0
A16
Text Label 4200 5900 2    60   ~ 0
A14
Text Label 4200 6200 2    60   ~ 0
A12
Text Label 4200 6300 2    60   ~ 0
A10
Wire Wire Line
	4200 5300 3800 5300
Wire Wire Line
	3800 5400 4200 5400
Wire Wire Line
	4200 5500 3800 5500
Wire Wire Line
	3800 5800 4200 5800
Wire Wire Line
	4200 5900 3800 5900
Wire Wire Line
	3800 6200 4200 6200
Wire Wire Line
	4200 6300 3800 6300
Text Label 2200 6500 0    60   ~ 0
A8
Wire Wire Line
	2200 6500 2600 6500
Text Label 2200 5800 0    60   ~ 0
A6
Text Label 2200 5700 0    60   ~ 0
A4
Text Label 2200 5400 0    60   ~ 0
A2
Text Label 2200 5300 0    60   ~ 0
A0
Text Label 2200 5100 0    60   ~ 0
A1
Text Label 2200 5000 0    60   ~ 0
A3
Text Label 2200 4700 0    60   ~ 0
A5
Text Label 2200 4600 0    60   ~ 0
A7
Text Label 2200 4300 0    60   ~ 0
A9
Text Label 2200 4200 0    60   ~ 0
A11
Wire Wire Line
	2600 4200 2200 4200
Wire Wire Line
	2200 4300 2600 4300
Wire Wire Line
	2600 4600 2200 4600
Wire Wire Line
	2200 4700 2600 4700
Wire Wire Line
	2600 5000 2200 5000
Wire Wire Line
	2200 5100 2600 5100
Wire Wire Line
	2200 5300 2600 5300
Wire Wire Line
	2600 5400 2200 5400
Wire Wire Line
	2200 5700 2600 5700
Wire Wire Line
	2600 5800 2200 5800
Text Label 2200 5200 0    60   ~ 0
TSR
Text Label 4200 5200 2    60   ~ 0
10X
Wire Wire Line
	4200 5200 3800 5200
Wire Wire Line
	2200 5200 2600 5200
Text Label 1550 2550 0    60   ~ 0
HGND
Text Label 3550 2550 0    60   ~ 0
HGND
Text Label 2650 2550 2    60   ~ 0
P0
Text Label 2650 2450 2    60   ~ 0
P4
Text Label 2650 2350 2    60   ~ 0
P8
Text Label 1550 2450 0    60   ~ 0
P2
Text Label 1550 2350 0    60   ~ 0
P6
Text Label 1550 2250 0    60   ~ 0
P10
Text Label 2650 2250 2    60   ~ 0
P12
Text Label 1550 2150 0    60   ~ 0
A0
Text Label 2650 2150 2    60   ~ 0
A1
Text Label 1550 2050 0    60   ~ 0
A2
Text Label 2650 2050 2    60   ~ 0
A3
Text Label 1550 1950 0    60   ~ 0
A4
Text Label 2650 1950 2    60   ~ 0
A5
Text Label 1550 1850 0    60   ~ 0
A6
Text Label 2650 1850 2    60   ~ 0
A7
Text Label 1550 1750 0    60   ~ 0
A8
Text Label 2650 1750 2    60   ~ 0
A9
Text Label 2650 1650 2    60   ~ 0
TSR
Text Label 4650 2550 2    60   ~ 0
P1
Text Label 3550 2450 0    60   ~ 0
P3
Text Label 4650 2450 2    60   ~ 0
P5
Text Label 3550 2350 0    60   ~ 0
P7
Text Label 4650 2350 2    60   ~ 0
P9
Text Label 3550 2250 0    60   ~ 0
P11
Text Label 4650 2250 2    60   ~ 0
P13
Text Label 3550 2050 0    60   ~ 0
A13
Text Label 4650 1650 2    60   ~ 0
10X
Text Label 1550 1650 0    60   ~ 0
A10
Text Label 4650 2150 2    60   ~ 0
A12
Text Label 4650 2050 2    60   ~ 0
A14
Text Label 4650 1950 2    60   ~ 0
A16
Text Label 4650 1850 2    60   ~ 0
A18
Text Label 4650 1750 2    60   ~ 0
A20
Text Label 3550 1950 0    60   ~ 0
A15
Text Label 3550 1850 0    60   ~ 0
A17
Text Label 3550 1750 0    60   ~ 0
A19
Text Label 3550 1650 0    60   ~ 0
A21
Text Label 3550 2150 0    60   ~ 0
A11
Wire Wire Line
	2650 1650 2350 1650
Wire Wire Line
	2350 1750 2650 1750
Wire Wire Line
	2650 1850 2350 1850
Wire Wire Line
	2350 1950 2650 1950
Wire Wire Line
	2650 2050 2350 2050
Wire Wire Line
	2350 2150 2650 2150
Wire Wire Line
	2650 2250 2350 2250
Wire Wire Line
	2350 2350 2650 2350
Wire Wire Line
	2650 2450 2350 2450
Wire Wire Line
	2350 2550 2650 2550
Wire Wire Line
	1850 1650 1550 1650
Wire Wire Line
	1550 1750 1850 1750
Wire Wire Line
	1850 1850 1550 1850
Wire Wire Line
	1550 1950 1850 1950
Wire Wire Line
	1550 2050 1850 2050
Wire Wire Line
	1550 2150 1850 2150
Wire Wire Line
	1850 2250 1550 2250
Wire Wire Line
	1550 2350 1850 2350
Wire Wire Line
	1850 2450 1550 2450
Wire Wire Line
	1550 2550 1850 2550
Wire Wire Line
	4650 1650 4350 1650
Wire Wire Line
	4350 1750 4650 1750
Wire Wire Line
	4650 1850 4350 1850
Wire Wire Line
	4650 1950 4350 1950
Wire Wire Line
	4650 2050 4350 2050
Wire Wire Line
	4650 2150 4350 2150
Wire Wire Line
	4650 2250 4350 2250
Wire Wire Line
	4350 2350 4650 2350
Wire Wire Line
	4650 2450 4350 2450
Wire Wire Line
	4350 2550 4650 2550
Wire Wire Line
	3850 2550 3550 2550
Wire Wire Line
	3550 2450 3850 2450
Wire Wire Line
	3850 2350 3550 2350
Wire Wire Line
	3550 2250 3850 2250
Wire Wire Line
	3850 2150 3550 2150
Wire Wire Line
	3550 2050 3850 2050
Wire Wire Line
	3850 1950 3550 1950
Wire Wire Line
	3550 1850 3850 1850
Wire Wire Line
	3850 1750 3550 1750
Wire Wire Line
	3550 1650 3850 1650
Text Label 2200 6300 0    60   ~ 0
HGND
Text Label 2200 6100 0    60   ~ 0
HGND
Text Label 2200 6000 0    60   ~ 0
HGND
Text Label 2200 5600 0    60   ~ 0
HGND
Text Label 2200 4800 0    60   ~ 0
HGND
Text Label 2200 4400 0    60   ~ 0
HGND
$EndSCHEMATC
