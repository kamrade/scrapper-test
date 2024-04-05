import random
import time

def sleep():
  value = random.random()
  scaled_value = 1 + (value * (9 - 5))
  time.sleep(scaled_value)