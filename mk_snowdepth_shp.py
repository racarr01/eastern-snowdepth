import shapefile
import time
import urllib
import xml.dom.minidom
import csv
import sys


def extractAddress(row):
  # This extracts an address from a row and returns it as a string. This requires knowing
  # ahead of time what the columns are that hold the address information.
  return '%s,%s,%s,%s,%s' % (row['Address1'], row['Address2'], row['City'], row['State'], row['Zip'])

def getCoords(row):
  # This pulls lat/longs and returns as string
  return '%s,%s' % (row['Longitude'], row['Latitude'])

def createPlacemark(kmlDoc, row, order):
  # This creates a  element for a row of data.
  # A row is a dict.
  placemarkElement = kmlDoc.createElement('Placemark')
  nameElement = kmlDoc.createElement('name')
  #print row['Amount']
  intAmount = int(float(row['Amount']))
  strAmount = str(intAmount)
  nameText = kmlDoc.createTextNode(strAmount)
      #row['Amount'])
  nameElement.appendChild(nameText)
  placemarkElement.appendChild(nameElement)
  styleElement = kmlDoc.createElement('styleUrl')
  styleText = kmlDoc.createTextNode('#m_snowsymbol0')
  styleElement.appendChild(styleText)
  placemarkElement.appendChild(styleElement)
  extElement = kmlDoc.createElement('ExtendedData')
  placemarkElement.appendChild(extElement)

  # Loop through the columns and create a  element for every field that has a value.
  for key in order:
    if row[key]:
      dataElement = kmlDoc.createElement('Data')
      dataElement.setAttribute('name', key)
      valueElement = kmlDoc.createElement('value')
      dataElement.appendChild(valueElement)
      valueText = kmlDoc.createTextNode(row[key])
      valueElement.appendChild(valueText)
      extElement.appendChild(dataElement)
  
  pointElement = kmlDoc.createElement('Point')
  placemarkElement.appendChild(pointElement)
  #coordinates = geocoding_for_kml.geocode(extractAddress(row))
  coordinates = getCoords(row)
  coorElement = kmlDoc.createElement('coordinates')
  coorElement.appendChild(kmlDoc.createTextNode(coordinates))
  pointElement.appendChild(coorElement)
  return placemarkElement


def createKML(csvReader, fileName, order):
  # This constructs the KML document from the CSV file.
  kmlDoc = xml.dom.minidom.Document()
  
  kmlElement = kmlDoc.createElementNS('http://earth.google.com/kml/2.2', 'kml')
  kmlElement.setAttribute('xmlns','http://earth.google.com/kml/2.2')
  kmlElement = kmlDoc.appendChild(kmlElement)
  documentElement = kmlDoc.createElement('Document')

  #NetworkLinkControl
  NLCElement = kmlDoc.createElement('NetworkLinkControl')

  minRefreshPeriodElement = kmlDoc.createElement('minRefreshPeriod')
  minRefreshPeriodText = kmlDoc.createTextNode('3600')
  minRefreshPeriodElement.appendChild(minRefreshPeriodText)
  NLCElement.appendChild(minRefreshPeriodElement)

  expiresElement = kmlDoc.createElement('expires')
  now = time.time()
  future = time.gmtime(now + (60 * 60 * 24.15))
  y = future[0]
  mo = future[1]
  d = future[2]
  h = future[3]
  mi = future[4]
  s = future[5]
  iso8601 = '%04d-%02d-%02dT%02d:%02d:%02dZ' % (y,mo,d,h,mi,s)
    
  expiresText = kmlDoc.createTextNode(str(iso8601))
  expiresElement.appendChild(expiresText)
  NLCElement.appendChild(expiresElement)
  
  now = time.gmtime(now)
  y = now[0]
  mo = now[1]
  d = now[2]
  h = now[3]
  mi = now[4]
  iso8601 = '%04d-%02d-%02dT%02d:%02dZ' % (y,mo,d,h,mi)

  messageElement = kmlDoc.createElement('message')
  messageText = kmlDoc.createTextNode('Snowdepth data refreshed at '+ str(iso8601))
  messageElement.appendChild(messageText)
  NLCElement.appendChild(messageElement)
  
  
  kmlElement.appendChild(NLCElement)
  #end NetworkLinkControl
  

  #snowsymbol 0 style

  styleElement = kmlDoc.createElement('Style')
  styleElement.setAttribute("id", "s_snowsymbol0")

  iconstyleElement = kmlDoc.createElement('IconStyle')
  scaleElement = kmlDoc.createElement('scale')
  scaleText = kmlDoc.createTextNode('0.8')
  scaleElement.appendChild(scaleText)
  iconstyleElement.appendChild(scaleElement)
  iconElement = kmlDoc.createElement('Icon')
  hrefElement = kmlDoc.createElement('href')
  hrefText = kmlDoc.createTextNode('http://maps.google.com/mapfiles/kml/pal4/icon43.png')
  hrefElement.appendChild(hrefText)
  iconElement.appendChild(hrefElement)
  iconstyleElement.appendChild(iconElement)

  hotSpotElement = kmlDoc.createElement('hotSpot')
  hotSpotElement.setAttribute("x","20")
  hotSpotElement.setAttribute("y","2")
  hotSpotElement.setAttribute("xunits","pixels")
  hotSpotElement.setAttribute("yunits","pixels")
  iconstyleElement.appendChild(hotSpotElement)
  labelstyleElement = kmlDoc.createElement('LabelStyle')
  scaleElement = kmlDoc.createElement('scale')
  scaleText = kmlDoc.createTextNode('0.8')
  scaleElement.appendChild(scaleText)
  labelstyleElement.appendChild(scaleElement)
  styleElement.appendChild(labelstyleElement)
  styleElement.appendChild(iconstyleElement)
  
#balloonstyle
  balloonstyleElement = kmlDoc.createElement('BalloonStyle')
  textElement = kmlDoc.createElement('text')
  
  CDATAElement = kmlDoc.createCDATASection('Name: $[Name]\012 <br /> Station ID: \
  $[Station_Id]\012 <br /> Date: $[DateTime_Report(UTC)]\012 <br /> Snowdepth: $[Amount] \
  $[Units]\012 <br /> Latitude: $[Latitude]\012 <br /> Longitude: $[Longitude]\012 <br />Elevation: \
  $[Elevation]\012 <br /><a href=\"http://forecast.weather.gov/MapClick.php?&textField1=$[Latitude]&textField2=$[Longitude]\"> \
  7-Day Forecast from NWS</a>')
 
  
  
  textElement.appendChild(CDATAElement)
  balloonstyleElement.appendChild(textElement)
  
  styleElement.appendChild(balloonstyleElement)
  #end balloonstyle
  
  documentElement.appendChild(styleElement)
  #end snowsymbol0 style

  
  #snowsymbol_hl0 style

  styleElement = kmlDoc.createElement('Style')
  styleElement.setAttribute("id", "s_snowsymbol_hl0")

  iconstyleElement = kmlDoc.createElement('IconStyle')
  scaleElement = kmlDoc.createElement('scale')
  scaleText = kmlDoc.createTextNode('1.0')
  scaleElement.appendChild(scaleText)
  iconstyleElement.appendChild(scaleElement)
  iconElement = kmlDoc.createElement('Icon')
  hrefElement = kmlDoc.createElement('href')
  hrefText = kmlDoc.createTextNode('http://maps.google.com/mapfiles/kml/pal4/icon43.png')
  hrefElement.appendChild(hrefText)
  iconElement.appendChild(hrefElement)
  iconstyleElement.appendChild(iconElement)
  hotSpotElement = kmlDoc.createElement('hotSpot')
  hotSpotElement.setAttribute("x","20")
  hotSpotElement.setAttribute("y","2")
  hotSpotElement.setAttribute("xunits","pixels")
  hotSpotElement.setAttribute("yunits","pixels")
  iconstyleElement.appendChild(hotSpotElement)
  labelstyleElement = kmlDoc.createElement('LabelStyle')
  scaleElement = kmlDoc.createElement('scale')
  scaleText = kmlDoc.createTextNode('1.0')
  scaleElement.appendChild(scaleText)
  labelstyleElement.appendChild(scaleElement)
  styleElement.appendChild(labelstyleElement)
  styleElement.appendChild(iconstyleElement)

#balloonstyle
  balloonstyleElement = kmlDoc.createElement('BalloonStyle')
  textElement = kmlDoc.createElement('text')
  
  CDATAElement = kmlDoc.createCDATASection('Name: $[Name]\012 <br /> Station ID: \
  $[Station_Id]\012 <br /> Date: $[DateTime_Report(UTC)]\012 <br /> Snowdepth: $[Amount] \
  $[Units]\012 <br /> Latitude: $[Latitude]\012 <br /> Longitude: $[Longitude]\012 <br />Elevation: \
  $[Elevation]\012 <br /><a href=\"http://forecast.weather.gov/MapClick.php?&textField1=$[Latitude]&textField2=$[Longitude]\"> \
  7-Day Forecast from NWS</a>')
  
  
  
  textElement.appendChild(CDATAElement)
  balloonstyleElement.appendChild(textElement)
  
  styleElement.appendChild(balloonstyleElement)
  #end balloonstyle
  documentElement.appendChild(styleElement)
  #end snowsymbol_hl0 style

  #stylemap creation
  stylemapElement = kmlDoc.createElement('StyleMap')
  stylemapElement.setAttribute("id", "m_snowsymbol0")

  pairElement = kmlDoc.createElement('Pair')

  keyElement = kmlDoc.createElement('key')
  keyText = kmlDoc.createTextNode('normal')
  keyElement.appendChild(keyText)
  pairElement.appendChild(keyElement)

  styleUrlElement = kmlDoc.createElement('styleUrl')
  styleUrlText = kmlDoc.createTextNode('#s_snowsymbol0')
  styleUrlElement.appendChild(styleUrlText)
  pairElement.appendChild(styleUrlElement)

  stylemapElement.appendChild(pairElement)

  pairElement = kmlDoc.createElement('Pair')

  keyElement = kmlDoc.createElement('key')
  keyText = kmlDoc.createTextNode('highlight')
  keyElement.appendChild(keyText)
  pairElement.appendChild(keyElement)

  styleUrlElement = kmlDoc.createElement('styleUrl')
  styleUrlText = kmlDoc.createTextNode('#s_snowsymbol_hl0')
  styleUrlElement.appendChild(styleUrlText)
  pairElement.appendChild(styleUrlElement)

  stylemapElement.appendChild(pairElement)
  documentElement.appendChild(stylemapElement)
  
  #end stylemap
  
  
  documentElement = kmlElement.appendChild(documentElement)

  
  
  
  # Skip the header line.
  csvReader.next()
  csvReader.next()
  
  for row in csvReader:
    if float(row['Longitude']) > -97.25 and int(float(row['Amount'])) > 0:  
      placemarkElement = createPlacemark(kmlDoc, row, order)
      documentElement.appendChild(placemarkElement)
  kmlFile = open(fileName, 'w')
  kmlFile.write(kmlDoc.toprettyxml('  ', newl = '\n', encoding = 'utf-8'))


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
  #kml = createKML(reader, '/usrls -ll /home/racarr/transfer/snowdepth.kml', order)
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

