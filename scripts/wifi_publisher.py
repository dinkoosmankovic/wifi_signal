#!/usr/bin/env python

import roslib; roslib.load_manifest('wifi_signal')
import rospy, os, re
import subprocess
from wifi_signal.msg import Wifi

class WifiNode():
	def __init__(self):
		pub = rospy.Publisher('wifi_signal', Wifi, queue_size=10)

		r = rospy.Rate(rospy.get_param('~rate', 1))
		interface = rospy.get_param('interface', "wlo1")
		
		while not rospy.is_shutdown():
			cmd = [ 'iwconfig', interface ]
			wifiraw = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0]
			essids = re.findall("ESSID:\"(.*)\"", wifiraw)
			addresses = re.findall("Access Point: ([0-9A-F:]{17})", wifiraw)
			signals = re.findall("Signal level=.*?([0-9]+)", wifiraw)
			link = re.findall("Link Quality=.*?([0-9]+)", wifiraw)
			bitrate = re.findall("Bit Rate=.*?([0-9]+)", wifiraw)
			
			msg = Wifi()

			for i in range(len(essids)):
				if (True):
					msg.MAC = addresses[0] 
					msg.dB = int(signals[0])
					msg.LinkQuality = int(link[0])
					msg.BitRate = int(bitrate[0])

			pub.publish(msg)
			r.sleep()

if __name__ == '__main__':
	rospy.init_node('wifi_signal_node_py')
	try:
		node = WifiNode()
	except rospy.ROSInterruptException: pass
	
