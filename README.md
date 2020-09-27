# waveforms.sh

Usage: `./waveforms.sh <formula>`

Using ffmpeg (that is a dependency), generate an mp4 file showing the waveform.

## &lt;formula&gt; syntax

The syntax of the &lt;formula&gt; is described
[here](https://ffmpeg.org/ffmpeg-all.html#Expression-Evaluation) and
[there](https://ffmpeg.org/ffmpeg-all.html#aevalsrc).

If you have the documentation files for ffmpeg you can see those by typing
`man ffmpeg` inside a terminal.

Also the comma needs to be separated. If you want to compute the arctangent
between x and y you SHOULD NOT type `atan2(x,y)` but instead `atan2(x\,y)`.

## Example

In the directory wave001 there is an example. Maybe in the future I will
commit some more, or maybe not. It depends on my will to improve this project.

Also I'd like to extend (I have to figure out how) the syntax so you can define
your own function (for example there are the functions `bitand(,)` and
`bitor(,)` but there is not `bitnot()` nor `bitxor(,)`)
