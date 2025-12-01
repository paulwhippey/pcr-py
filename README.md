# pcr-py

A quick and dirty Python script to control the Icom PCR-1000 receiver with a Mac or Linux machine.

Many, many thanks to GM4JJJ for publishing the protocol for this radio! This would have been impossible otherwise. URL to the GM4JJJ website is here: [http://www.gm4jjj.co.uk/PCR1000.html](http://www.gm4jjj.co.uk/PCR1000.html)

## Dependencies

Needs pyserial and a working USB to serial adapter. Add your USB adapter device path into the script at the serialPort variable.

## How To Use

Currently, the quick and dirty command syntax is:

python ./pcr000.py G MMM KKK HHH mm ff

Where:
G = GHz, MMM = MHz, KKK = kHz, HHH = Hz, mm = mode, ff = filter

Mode is one of:
- 00 = LSB
- 01 = USB
- 02 = AM
- 03 = CW
- 04 = Not used or Unknown
- 05 = NFM
- 06 = WFM

Filter is one of:
- 00 = 3 Khz (actually 2.8 Khz) (CW USB LSB AM)
- 01 = 6 Khz (CW USB LSB AM NFM)
- 02 = 15 Khz (AM NFM)
- 03 = 50 Khz (AM NFM WFM)
- 04 = 230 Khz (WFM)

### Example

```
python ./pcr1000.py 0 088 900 000 06 04
```
