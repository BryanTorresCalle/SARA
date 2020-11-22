
import time
import spidev

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000
def getTemperature():
    stop = time.time() + 600
    tt = []

    while time.time() < stop:
        d = spi.readbytes(2)
        if d[0]:
            word = (d[0]<<8) | d[1]
            if (word & 0x8006) == 0: # Bits 15, 2, and 1 should be zero.
                t = (word >> 3)/4.0
                #tt.append(t)
                #print("{:.2f}".format(t))
                return t
                
            else:
                print("bad reading {:b}".format(word))
                return
        

