#!/bin/sh
HOMEDIR=/usr/home/racarr
WRKFILDIR=$HOMEDIR/gis_data/snowdepth
HTDOCS=/usr/jail/www/usr/local/www/apache24/data/ssl
/usr/local/bin/python $HOMEDIR/scripts/mk_snowdepth_csv.py
#turn csv to json
/usr/local/bin/ogr2ogr -f GeoJSON $WRKFILDIR/snowdepth_geo.json $WRKFILDIR/snowdepth_new.vrt 
#load json into postgres
/usr/local/bin/ogr2ogr -t_srs EPSG:3857 -s_srs EPSG:4326 -overwrite -f "PostgreSQL" PG:"dbname=op_gis user=racarr" $WRKFILDIR/snowdepth_geo.json
/bin/rm $HTDOCS//maps/bootleaf/assets/json/snowdepth.json
/bin/rm $WRKFILDIR/snowdepth_topo.json

/bin/cp $WRKFILDIR/snowdepth_geo.json $HTDOCS/maps/bootleaf/assets/json/snowdepth.json
/usr/local/bin/topojson -p -o $WRKFILDIR/snowdepth_topo.json $WRKFILDIR/snowdepth_geo.json
