#!/usr/bin/env python
import argparse
import pathlib
import struct
import sys

def main(args):
	out_dir = args.out_dir
	sys.path.insert(0, out_dir)
	import waveform
	total_time = args.total_time
	sampling_rate = args.sampling_rate
	dt = 1/sampling_rate
	s = struct.Struct("<f")
	with open(pathlib.Path(out_dir).joinpath("audio.raw"), "wb") as f:
		with open(pathlib.Path(out_dir).joinpath("time_axis"), "wb") as f_t:
			n, t = 0, 0
			while t < total_time:
				print("\rCreating audio file ... {:6.2f}%".
		  				format(t/total_time*100), end="")
				to_write = s.pack(waveform.f(t, total_time, n, sampling_rate))
				t_write = s.pack(t)
				f_t.write(t_write)
				f.write(to_write)
				n += 1
				t += dt
	print("\rCreating audio file ... 100.00%")
	print("DONE.")

if __name__ == "__main__":
	ap = argparse.ArgumentParser()
	ap.add_argument("out_dir")
	ap.add_argument("total_time", type=float)
	ap.add_argument("sampling_rate", type=int)
	main(ap.parse_args())
