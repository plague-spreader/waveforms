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
	dt = 2/sampling_rate # see Claude-Shannon sampling theorem
	s = struct.Struct("<f")
	with open(pathlib.Path(out_dir).joinpath("audio.raw"), "wb") as f:
		n, t = 0, 0
		while t < total_time:
			print("\rCreating audio file ... {:6.2f}%".format(t/total_time*100), end="")
			to_write = s.pack(waveform.f(t, total_time, n, sampling_rate))
			f.write(to_write) # see Claude-Shannon sampling theorem
			f.write(to_write) # see Claude-Shannon sampling theorem
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
