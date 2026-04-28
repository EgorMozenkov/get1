import RPi.GPIO as GPIO
import time

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time=0.01, verbose=False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time
        
        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21
        
        GPIO.setmode(GPIO.BCM)
        for pin in self.bits_gpio:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)
        GPIO.setup(self.comp_gpio, GPIO.IN)
    
    def deinit(self):
        for pin in self.bits_gpio:
            GPIO.output(pin, 0)
        GPIO.cleanup()
    
    def number_to_dac(self, number):
        bits = [int(bit) for bit in bin(number)[2:].zfill(8)]
        for i in range(8):
            GPIO.output(self.bits_gpio[i], bits[i])
        if self.verbose:
            print(f"  ЦАП: число {number}, биты {bits}")
    
    def sequential_counting_adc(self):
        for number in range(256):
            self.number_to_dac(number)
            time.sleep(self.compare_time)
            
            comp_value = GPIO.input(self.comp_gpio)
            if self.verbose:
                print(f"    число={number}, comp={comp_value}")
            
            if comp_value == 1: 
                return number
        
        return 255
    
    def get_sc_voltage(self):
        number = self.sequential_counting_adc()
        voltage = (number / 255) * self.dynamic_range
        if self.verbose:
            print(f"Измерено: число={number}, напряжение={voltage:.3f} В")
        return voltage

if __name__ == "__main__":
    DYNAMIC_RANGE = 3.3 
    
    try:
        adc = R2R_ADC(DYNAMIC_RANGE, compare_time=0.01, verbose=True)
        
        while True:
            voltage = adc.get_sc_voltage()
            print(f"Напряжение на потенциометре: {voltage:.3f} В")
            time.sleep(0.5) 
            
    except KeyboardInterrupt:
        print("\nОстановка")
    finally:
        adc.deinit()