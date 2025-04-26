#!/bin/bash
#bash image-batch-wget.sh {S3_KEY FILE} {OUTPUT_DIRECTORY}

# Progress bar
function ProgressBar {
    let _progress=(${1}*100/${2}*100)/100
    let _done=(${_progress}*4)/10
    let _left=40-$_done
    _fill=$(printf "%${_done}s")
    _empty=$(printf "%${_left}s")
printf "\rProgress : [${_fill// /#}${_empty// /-}] ${_progress}%%"
}

# Download images
DIR=$2
curstart=1
i=0
j=0
pb_start=1
pb_end=`wc -l $1`

tail -n +"$curstart" $1 |while read X; do
    (aws s3 cp s3://my-bucket/$X/raw $DIR/$X.jpeg --quiet --debug &&
     F=`echo $X|sed 's/.*\///'`.jpeg &&
     convert $DIR/$F -resize 640\> ttt2/$F &&
     mv ttt2/$F $DIR/$F;
     )&
    i=$((i+1))
    j=$((j+1))
    if [ $i -gt 19 ]; then
        i=0
        wait
    fi
    ProgressBar "$j" ${pb_end}
done