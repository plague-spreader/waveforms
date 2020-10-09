#!/usr/bin/env python

import math

def f(t, n, s):
	return math.sin(t*((int(n**1.01)<<3)^(int(n**0.99)>>5))/s*2)
