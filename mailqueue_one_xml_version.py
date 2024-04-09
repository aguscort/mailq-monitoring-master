#!/usr/bin/env python
######## -*- coding: utf-8 -*
import os, sys, time
import xml.etree.ElementTree as ET

xmlPath = '/home/opsmon/scripts/mailq/status/'
xmlFile = 'mailq_alert.xml'

# Servers
servers = ['ha-relaymail', 'ha-smtp-prod', 'ha-relaymaildmz']

root = ET.Element('mailqueue')
comment = ET.Comment(
    'This XML is generated by a script called mailqueue.py at ocvlp-bmc014. In case of malfunction or further changes check the script there.'
)
root.insert(1, comment)
root.set('time', str(time.time()))

for server in servers:
    serverCommand = "ssh " + server + " sudo mailq | tail -1| awk '{$4= \" \"; print $3}'"
    value = os.popen(serverCommand).read()
    value = value.split("\n")[0]
    # Added info into the XML
    alert = ET.SubElement(root, 'alert')
    alert.set('server', server)
    ET.SubElement(alert, 'itemsQueued').text = str(value)
    if (int(value) > 300):
        ET.SubElement(alert, 'status').text = 'NotOK'
    else:
        ET.SubElement(alert, 'status').text = 'OK'

dataAlarm = ET.tostring(root).decode("utf-8")
fileAlarm = open(xmlPath + xmlFile, 'w')
fileAlarm.write(dataAlarm)
fileAlarm.close()
