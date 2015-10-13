#!/bin/bash
# Author: Sarah Heim
# Description: nccopy ALL files in subdirectories with ONLY specific extension

echo ${PWD}
for x in "../../netcdfs/*/*_qc2.nc" # <------ with this extension
do
  full = $(readlink -f "$x")
  echo $x $full
  new=$(echo $x | sed -e 's/\.nc$/_nccopy.nc/')
  echo "  1 nccopying:  " $x $new
  nccopy $x $new
  #sleep 1m
  echo "  2 overwriting new nccopy to original"
  mv -f $new $x 
  echo "  3 done:" $x
done
