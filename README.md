# meshtastic
Random scripts

NOAA Alerts
  Requires the meshtastic python CLI installed.
  Run the createdb script first to create the sqlite DB.
  Edit the main script to change location and meshtastic usb info.
  Run main script, it will pull down any current alerts and send the formated alert to the mesh.
    It will then write the ID of the alert to the DB so that each alert is only sent once.
  Schedule to run as often as you wish, 5 minutes is probably enough.
