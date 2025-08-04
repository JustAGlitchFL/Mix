import board
import analogio
import digitalio
import time
import pwmio
import busio
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# SPI MCP3008
spi = board.SPI()
cs = digitalio.DigitalInOut(board.D5)  # Chip select pin
mcp = MCP.MCP3008(spi, cs)
# analog input channels
chan0 = AnalogIn(mcp, MCP.P0)
chan1 = AnalogIn(mcp, MCP.P1)
chan2 = AnalogIn(mcp, MCP.P2)
chan3 = AnalogIn(mcp, MCP.P3)
chan4 = AnalogIn(mcp, MCP.P4)
chan5 = AnalogIn(mcp, MCP.P5)
chan6 = AnalogIn(mcp, MCP.P6)
chan7 = AnalogIn(mcp, MCP.P7)

# constants
min_value = 340
max_value = 65535
range = max_value - min_value
samples = 10  # number of samples to average for noise reduction

# deej interfacing

def noise_reduction(channel, samples=samples):
    smooth_value = sum(channel.value for _ in range(samples))
    return (max(0, smooth_value - min_value) * 1023) 

def read_channels():
    return {
        'chan0': noise_reduction(chan0),
        'chan1': noise_reduction(chan1),
        'chan2': noise_reduction(chan2),
        'chan3': noise_reduction(chan3),
        'chan4': noise_reduction(chan4),
        'chan5': noise_reduction(chan5),
        'chan6': noise_reduction(chan6),
        'chan7': noise_reduction(chan7)
    }

def send_deej_values(values):
    print('|'.join(map(str, values)))

# main loop
while True:
    values = read_channels()
    send_deej_values(values)
    time.sleep(0.1)