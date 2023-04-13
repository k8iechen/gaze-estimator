#!/bin/bash

# Script info.
readonly PROGNAME=$(basename ${BASH_SOURCE[0]});
readonly PROGDIR=$(readlink -m $(dirname ${BASH_SOURCE[0]}));

readonly VID="$1"; shift;

# detect poses
$PROGDIR/OpenFace/build/bin/FaceLandmarkVidMulti -f $PROGDIR/Vid_Cal/${VID}.mp4 -out_dir $PROGDIR/processed
# convert result to MP4
mkdir -p $PROGDIR/int_landmarked
ffmpeg -y -loglevel info -i $PROGDIR/processed/${VID}.avi $PROGDIR/int_landmarked/${VID}.mp4

