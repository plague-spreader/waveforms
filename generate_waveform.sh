#!/bin/sh

[ $# -eq 0 ] && >&2 echo "Usage: $0 <formula>" && exit 1

[ -d wave001 ] && {
	new=$(printf "wave%03d" $(($(echo wave* | tail -c4)+1)))
} || new=wave001

mkdir $new
cd $new

echo $1 > formula.txt
ffmpeg -f lavfi -i "aevalsrc=$1" -filter_complex "[0:a]showwaves=mode=line:colors=white,format=yuv420p[v]" -map 0:a -map "[v]" out.mp4

mpv out.mp4

invalid_choice=1
while [ "$invalid_choice" ]; do
	echo -n "Are you ok with the results [Y/n]? "
	read choice

	[ "$choice" = "" -o "$choice" = y -o "$choice" = Y ] && 
		invalid_choice="" || {
		[ $choice = n -o $choice = N ] &&
		{ cd ..; rm -rf $new; invalid_choice=""; } || 
			>&2 echo "You have to input either y or n"
	}
done
