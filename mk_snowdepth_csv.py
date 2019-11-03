
import time
import urllib.request
import xml.dom.minidom
import csv
import sys

def main():
    # This reader opens up 'google-addresses.csv', which should be replaced with your own.
    # It creates a KML file called 'google.kml'.
  
    # If an argument was passed to the script, it splits the argument on a comma
    # and uses the resulting list to specify an order for when columns get added.
    # Otherwise, it defaults to the order used in the sample.
  
    timeHere = time.localtime()
    if timeHere[1] < 10:
        month = "0" + str(timeHere[1])
    else:
        month = str(timeHere[1])
    if timeHere[2] < 10:
        dayofmonth = "0" + str(timeHere[2])
    else:
        dayofmonth = str(timeHere[2])
    url1 = "http://www.nohrsc.noaa.gov/nsa/discussions_text/National/snowdepth/"
    url2 = url1 + str(timeHere[0]) + month + "/snowdepth_" + \
    str(timeHere[0]) + month + dayofmonth + "06_e.txt"
    urllib.request.urlretrieve(url2,'/usr/home/racarr/transfer/sd.txt')
    ipfieldnames = ['Station_Id','Name','Latitude','Longitude','Elevation', \
    'Physical_Element','DateTime_Report(UTC)','Amount','Units', \
    'Zip_Code']
    opfieldnames = ['Station_ID', 'Station_Nam', 'Latitude', 'Longitude', \
    'Snowdepth', 'Units', 'Rept_Date']
    with open('/usr/home/racarr/transfer/sd.txt', 'r', newline='') as csvfile1, \
        open('/usr/home/racarr/gis_data/snowdepth/snowdepth.csv', 'w', newline='') as csvfile:
            reader = csv.DictReader(csvfile1, fieldnames=ipfieldnames, delimiter='|')
            next(reader)
            next(reader)
            writer = csv.DictWriter(csvfile, fieldnames=opfieldnames)
            writer.writeheader()
            for row in reader:
                try:
                    if float(row['Longitude']) > -97.25 and int(float(row['Amount'])) > 0:
                        writer.writerow({'Station_ID': row['Station_Id'], \
                       'Station_Nam': row['Name'], 'Latitude': row['Latitude'],\
                       'Longitude': row['Longitude'], 'Snowdepth': row['Amount'],\
                       'Units': row['Units'], \
                       'Rept_Date': row['DateTime_Report(UTC)']})
                except (TypeError, ValueError):
                    print (row['Name'], repr(row['Longitude']), repr(row['Latitude']))
if __name__ == '__main__':
    main()
