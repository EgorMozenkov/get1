import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

dac_bits = [24, 22, 23, 27, 17, 25, 12, 16]

for pin in dac_bits:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

dynamic_range = 3.3

def voltage_to_number(voltage):
    if not (0.0 <= voltage <= dynamic_range):
        print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {dynamic_range:.2f} В)")
        print("Устанавливаем 0.0 В")
        return 0
    return int(voltage / dynamic_range * 255)

def number_to_dac(number):
    bits = [int(bit) for bit in bin(number)[2:].zfill(8)]
    for i in range(8):
        GPIO.output(dac_bits[i], bits[i])

try:
    while True:
        try:
            voltage = float(input("Введите напряжение в Вольтах: "))
            number = voltage_to_number(voltage)
            number_to_dac(number)
            print(f"Число: {number}, Двоичное: {bin(number)[2:].zfill(8)}")
        except ValueError:
            print("Вы ввели не число. Попробуйте ещё раз\n")

finally:
    GPIO.output(dac_bits, 0)
    GPIO.cleanup()