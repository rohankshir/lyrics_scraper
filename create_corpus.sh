#! /bin/bash

get_billboards=./billboards.py
billboards_playlist='r-b-hip-hop-songs'
num_songs=300

mkdir -p $billboards_playlist

for y in `seq 2000 2015`; do
    workdir=$billboards_playlist/$y
    mkdir -p $workdir
    rm $workdir/*
    songfile=$workdir/$billboards_playlist.$num_songs
    echo $songfile
    [ -e "$songfile" ] || $get_billboards "$y" "$num_songs" -c "$billboards_playlist" > "$songfile"
    # while read p; do
    # 	./genius.rb "$workdir" <<<$p
    # 	sleep 1
    # done <$songfile
    parallel -j 4 --gnu  -a "$songfile" "./genius.rb $workdir <<<{}"
done
