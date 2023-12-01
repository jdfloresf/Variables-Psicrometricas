import math
from multiprocessing import reduction
import re
import numpy as np

def temp_bulbo(t, W, Ws):
    tbh = (-599*W*t + 1006*t -2051000*Ws + 2051000*W)/(1006 / 2380*Ws)
    return tbh

print("tbh: ", temp_bulbo(20,0.00726, 0.0147))
