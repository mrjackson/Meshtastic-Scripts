#!/usr/bin/env python3
#https://api.weather.gov/alerts/active?point=38.8966079,-77.0401901

import datetime
import time
import requests
import json
import shlex
import subprocess
import sqlite3


lat = "38.8966079"
lon = "-77.0401901"
datetime = time.strftime("%m-%d-%Y %H:%M:%S", time.localtime())

response = requests.get(f'https://api.weather.gov/alerts/active?point={lat},{lon}').json()

conn = sqlite3.connect('~/data/meshtasticNOAA.sqlite')
c = conn.cursor()

for x in response['features']:
  #print("\n*****\n")
  #print("areaDesc: " + x['properties']['areaDesc'])
  #print(x['properties']['parameters']['NWSheadline'][0])
  #print("headline: " + x['properties']['headline'])
  #print("id: " + x['properties']['id'])
  #print(x['properties']['description'])

  try:
    txtarea = x['properties']['areaDesc']
  except:
    txtarea = ""

  try:
    txtheadline = x['properties']['parameters']['NWSheadline'][0]
  except:
    txtheadline = ""

  try:
    txturl = "https://weather.gov"
  except:
    txturl = ""

  msgText = "NOAA ALERT - " + txtheadline + " - " + txtarea + " - " + txturl
  if len(msgText) > 230:
    msgText = msgText[:225] + "..."
  print("alertText: " + msgText)

  #Check for existing ID in DB
  existAlert = c.execute ("""select count(*) from data where alertid == ?;""", (x['properties']['id'],))
  existAlertCount = (existAlert.fetchone()[0])
  if existAlertCount < 1:
    d = (datetime, x['properties']['id'])
    c.execute('insert into data values (?,?)', d)
    #Poin to meshtastic CLI install, set USB port and Channel Index
    subprocess.run(shlex.split("~/bin/meshtastic --port /dev/ttyUSB0 --ack --sendtext '" + msgText + "' --ch-index 1"))
    print("Sending Alert to the Mesh")
    break
  else:
    print("Alert already sent to Mesh")

  print("\n*****\n")

conn.commit()
c.close()
