#!/bin/sh
dt=`date +%m`
if [ $dt -eq 01 ]
then
    month="jan"
elif [ $dt -eq 02 ]
then
    month="feb"
elif [ $dt -eq 03 ]
then
    month="mar"
elif [ $dt -eq 04 ]
then
    month="apr"
elif [ $dt -eq 05 ]
then
    month="may"
elif [ $dt -eq 06 ]
then
    month="jun"
elif [ $dt -eq 07 ]
then
    month="jul"
elif [ $dt -eq 08 ]
then
    month="aug"
elif [ $dt -eq 09 ]
then
    month="sep"
elif [ $dt -eq 10 ]
then
    month="oct"
elif [ $dt -eq 11 ]
then
    month="nov"
elif [ $dt -eq 12 ]
then
    month="dec"
fi 
day=`date +%d`
year=`date +%Y`
filename=$day$month$year

cd /usr/home/racarr/github_projects/eastern_snowdepth
/bin/cp /usr/home/racarr/gis_data/snowdepth/snowdepth_topo.json ./
/usr/local/bin/git add ./snowdepth_topo.json
/usr/local/bin/git commit -m "${filename} update to snowdepth_topo.json"
/usr/local/bin/git push
cd /home/racarr
