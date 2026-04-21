import numpy as np
import time

def get_sin_wave_amplitude(freq, time_moment):
    """
    Возвращает нормализованное значение синуса (от 0 до 1)
    Формула: (sin(2πft) + 1) / 2
    """
    return (np.sin(2 * np.pi * freq * time_moment) + 1) / 2

def wait_for_sampling_period(sampling_frequency):
    """Ждёт один период дискретизации"""
    time.sleep(1 / sampling_frequency)