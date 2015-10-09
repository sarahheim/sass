#!/bin/bash
# Author: Sarah Heim
# Description: nccopy ALL files in subdirectories with ONLY specific extension

echo ${PWD}
for x in "../../netcdfs/*/*_qc2.nc" # <------ with this extension
do
  full= $(readlink -f "$x")
  echo "NAME:" $x $full
  MODDATE= stat -c %Y $x
  #MODDATE= $(stat -c %y "$x")
  #MODDATE=${MODDATE%% *}
  echo "MODDATE: " $MODDATE
  echo "DATE-now:" "$(date +%s)"
  #echo "TEST:" $(( $(stat -c %Y $x) - $NOW))
  #echo "TEST:" $(stat -c %Y $x) | awk '{print $1}'
  for d in `stat -c %Y $x`
  do
    NOW=$(date +"%s")
    #echo "NOW:" "$NOW"
    #echo "SEP:" $d "NOW:" "$NOW"
    #DIF= `expr $(date +%s) - $d`
    DIF=$(($NOW-$d))
    #DIF= $[ $(date +%s) - $d ]
    #echo "DIF:" "$DIF"
    echo "SEP:" $d "NOW:" "$NOW" "DIF:" "$DIF"
    #if [ "$DIF" < "200000" ]
    if [ $DIF -lt 200000 ]
    then
      echo "IF --- DO NCCOPY"
    else
      echo "else"
    fi
  done
  #DIF= `expr $NOW - $MODDATE`
  #declare -i DIF
  #DIF= $NOW-1000
  #echo "$[$NOW-$MODDATE]"
  #(( DIF= "$NOW"-1000 ))
  #echo "$DIF"
  echo "END"
  #new=$(echo $x | sed -e 's/\.nc$/_nccopy.nc/')
  #echo "  1 nccopying:  " $x $new
  #nccopy $x $new
  ##sleep 1m
  #echo "  2 overwriting new nccopy to original"
  #mv -f $new $x 
  #echo "  3 done:" $x
done
