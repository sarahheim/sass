#!/bin/bash
# Author: Sarah Heim
# Description: nccopy ALL files in subdirectories with ONLY specific extension

echo ${PWD}
START=$(date +"%s")
for x in ../../netcdfs/*/*_qc2.nc # <------ with this extension
do
  #full= $(readlink -f "$x")
  #echo "NAME:" $x $full
  mod=`stat -c %Y $x`
  #echo "TMP:" $mod
  NOW=$(date +"%s")
  DIF=$(($NOW-$mod))
  #echo "SEP:" $mod "NOW:" "$NOW" "DIF:" "$DIF"
  #ONLY nccopy files that have been updated in the last 48 hours
  recent=$((3600*48)) 
  if [ $DIF -lt $recent ]
  then
    echo "NCCOPY:" $x "$DIF"
    new=$(echo $x | sed -e 's/\.nc$/_nccopy.nc/')
    #echo $x "TEMP:" $new
    nccopy $x $new
    mv -f $new $x
  #else
  #  echo "else"
  fi
done
echo "DONE!" $(($(date +"%s")-$START))
