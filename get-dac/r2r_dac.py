import RPi.GPIO as GPIO

class R2R_DAC:
    def __init__(self, gpio_bits, dynamic_range, verbose=False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        
        GPIO.setmode(GPIO.BCM)
        for pin in self.gpio_bits:
            GPIO.setup(pin, GPIO.OUT, initial=0)
    
    def deinit(self):
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()
    
    def set_number(self, number):
        bits = [int(bit) for bit in bin(number)[2:].zfill(8)]
        for i in range(8):
            GPIO.output(self.gpio_bits[i], bits[i])
        if self.verbose:
            print(f"Установлено число: {number}, Двоичное: {bin(number)[2:].zfill(8)}")
    
    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {self.dynamic_range:.2f} В)")
            print("Устанавливаем 0.0 В")
            number = 0
        else:
            number = int(voltage / self.dynamic_range * 255)
        self.set_number(number)
        if self.verbose:
            print(f"Напряжение: {voltage:.2f} В -> Число: {number}")

if __name__ == "__main__":
    try:
        dac = R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.183, True)
        
        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)
            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")
    finally:
        dac.deinit()