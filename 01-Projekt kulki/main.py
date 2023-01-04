from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import machine
import utime

analog = machine.ADC(26)
MAX = 0

# rodzielczość wyświetlacza OLED
WIDTH = 128
HEIGHT = 32

# inicjacja I2C  na portach 26, 27
i2c = I2C(0, scl=Pin(27), sda=Pin(26), freq=200000)

# inicjacja instancji odpowiadającej wyświetlaczowi OLED
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

while True:
    reading = analog.read_u16()

    # wyliczanie ciężaru
    if reading >= 0 and reading < 17964:
        mass = reading / 183.31
    elif reading >= 17964 and reading < 36554:
        mass = (reading - 15937.5) / 20.68
    elif reading >= 36554 and reading <= 65535:
        mass = (reading - 28305.63) / 8.27

    # logika wyświetlania chwilowej wartości MAX przez 3 sekundy od zarejestrowania maksymalnego pomiaru
    if mass > MAX:
        MAX = mass
        timer = utime.time()
    else:
        if utime.time() - timer > 3:
            MAX = mass
        else:
            pass

    # czyszczenie ekranu
    oled.fill(0)

    # wyświetlanie sformatowanego tekstu
    oled.text("Curr:\t{} g".format(round(mass, 2)), 5, 8)
    oled.text('MAX:\t{} g'.format(round(mass, 2)), 5, 18)

    # "wgranie" na wyświetlacz tekstu
    oled.show()