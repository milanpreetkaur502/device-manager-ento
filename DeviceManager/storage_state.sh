#!/bin/sh

OUTFILE="/tmp/storage"

#while [ true ]
#do
total=$(df -h /dev/mmcblk1p1 | awk 'NR>1 {print $2 | "sort -r -k3 -n"}')
used=$(df -h /dev/mmcblk1p1 | awk 'NR>1 {print $3 | "sort -r -k3 -n"}')
available=$(df -h /dev/mmcblk1p1 | awk 'NR>1 {print $4 | "sort -r -k3 -n"}')
avi_files=$(ls /media/mmcblk1p1/upload/ | grep -i .avi | wc -l)
mjpg_files=$(ls /media/mmcblk1p1/upload/ | grep -i .mjpg | wc -l)

files=$(($avi_files+$mjpg_files))
echo "{
	\"total\":\"$total\",
	\"used\":\"$used\",
	\"available\":\"$available\",
	\"files\":\"$files\"
}" > $OUTFILE
#sleep 60
#done
