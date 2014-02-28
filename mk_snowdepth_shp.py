import shapefile
import time
import urllib
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
                       
  #print timeHere
  url1 = "http://www.nohrsc.noaa.gov/nsa/discussions_text/National/snowdepth/"
  url2 = url1 + str(timeHere[0]) + month + "/snowdepth_" + str(timeHere[0]) + month + dayofmonth + "06_e.txt"
  urllib.urlretrieve(url2,'/usr/home/racarr/transfer/sd.txt')
  
  # set variable for shapefile writer
  w = shapefile.Writer(shapefile.POINT) 
  w.field('Station_ID', 'C', '20')
  w.field('Station_Nam','C','40')
  w.field('Snowdepth', 'N', 6, 3)
  w.field('Units', 'C', '10')
  w.field('Rept_Date', 'C', '20')
  # csv.register_dialect('snowdata', delimiter = '|')
  order = ['Station_Id', 'Name', 'Latitude', 'Longitude', 'Elevation', 'Physical_Element', 'DateTime_Report(UTC)', 'Amount', 'Units', 'Zip_Code']
  reader = csv.DictReader(open('/usr/home/racarr/transfer/sd.txt'), order, delimiter='|')
  reader.next()
  reader.next()
  for row in reader:
    #print reader.next()
    #print row['Longitude']
    if float(row['Longitude']) > -97.25 and int(float(row['Amount'])) > 0:
      w.point(float(row['Longitude']),float(row['Latitude']))
      w.record(row['Station_Id'],row['Name'],float(row['Amount']), row['Units'], row['DateTime_Report(UTC)'])
  #print reader.next()
  w.save('/usr/home/racarr/shapefiles/test/snowdepth_geo')
if __name__ == '__main__':
  main()

