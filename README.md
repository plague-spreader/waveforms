# waveforms

Usage: `./generate_waveform.sh <directory> <total time> <sampling rate> [keep]`

This script creates a raw audio file with the specified `<sampling rate>` from the function `f(., ., .)` which must be inside `waveform.py` which must be inside `<directory>`.
Then it creates a video with that audio file showing the waveform. The video duration will be `<total time>` seconds.

If a fourth parameter is passed (the `[keep]` parameter) then the time axis and the raw audio data
is kept for plotting (See `How to plot the raw audio data` subsection)

## What must be inside &lt;directory&gt;/waveform.py 

This python file MUST HAVE a function `f` which returns a floating point.

The function `f` MUST HAVE three parameters which are:

- the time variable
- the sample number (starting from 0)
- the sampling frequency

You can use these three variables and you can use any sub-function you want, as long you return a floating point.

## How to plot the raw audio data

Just go to the waveform directory and run `plot_raw_data.py`

## Dependencies

- [ffmpeg](https://ffmpeg.org/)
- [argparse](https://pypi.org/project/argparse/)
- [pathlib](https://pypi.org/project/pathlib/)
- [matplotlib](https://pypi.org/project/matplotlib/)

## Example

In the directory wave001 there is an example.
The example creates the waveform associated to the function `math.sin(t*((int(n**1.01)<<3)^(int(n**0.99)>>5))/s*2)` which is

Æ S T H E T I C

There is a more complex example in wave002
