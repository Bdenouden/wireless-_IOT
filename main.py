import matplotlib.pyplot
import pyshark
import sys
import os

mydir = os.path.dirname(__file__)

print('I live in: ' + mydir)


cap = pyshark.FileCapture(mydir + '/data/mycapture.pcapng')
dir (cap[0])
