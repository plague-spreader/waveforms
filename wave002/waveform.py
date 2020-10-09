import math
import struct

s = struct.Struct("<f")
def float2bits(x):
	ret = []
	for byte in s.pack(x):
		for i in range(7, -1, -1):
			ret.append(1 if byte & 1 << i else 0)
	return ret

def shift_left_by_n(arr, n=0):
	return arr[n::] + arr[:n:]

def shift_right_by_n(arr, n=0):
	return arr[n:len(arr):] + arr[0:n:]

def bitand(bits_left, bits_right):
	assert len(bits_left) == len(bits_right), "The arrays must have equal length"
	return [bits_left[i]&bits_right[i] for i in range(len(bits_left))]

def bitxor(bits_left, bits_right):
	assert len(bits_left) == len(bits_right), "The arrays must have equal length"
	return [bits_left[i]^bits_right[i] for i in range(len(bits_left))]

def bits2float(bits):
	ints = []
	for i in (0, 8, 16, 24):
		j, x = 7, 0
		for b in bits[i:i+8]:
			x += b*(1<<j)
			j -= 1
		ints.append(x)
	return s.unpack(bytes(ints))[0]

def sin(t, f):
	return math.sin(2*math.pi*f*t)

def f(t, T, n, s):
	tmp = bits2float(bitand(float2bits(math.sin(t/5+0.3)), float2bits(math.sin(t/3+1.4))))
	return sin(t*tmp, 220)
