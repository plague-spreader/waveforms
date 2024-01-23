#!/bin/sh

[ $# -lt 3 ] && >&2 echo "Usage $0 <directory> <total time> \
<sampling frequency>" && exit 1

wav_dir=$(realpath $1)
total_time=$2
sampling_frequency=$3
cd $wav_dir

../create_video.py $wav_dir $total_time $sampling_frequency

ffmpeg -f f32le -ar $sampling_frequency -i audio.raw \
-filter_complex "[0:a]showwaves=mode=line:colors=white,format=yuv420p[v]" \
-map 0:a -map "[v]" out.mp4
[ $# -eq 4 ] || rm -f audio.raw time_axis

mpv out.mp4

invalid_choice=1
while [ "$invalid_choice" ]; do
	echo -n "Are you ok with the results [Y/n]? "
	read choice

	[ "$choice" = "" -o "$choice" = y -o "$choice" = Y ] && 
		invalid_choice="" || {
		[ $choice = n -o $choice = N ] &&
		{ rm -rf out.mp4; invalid_choice=""; } || 
			>&2 echo "You have to input either y or n"
	}
done
