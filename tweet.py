#!/usr/bin/env python
import time

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from twython import Twython


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

# Count the amount of lines in the old and new lactos files
oldlen = file_len("/home/pi/lactobot/ncbi_files/lactos_old.txt")
newlen = file_len("/home/pi/lactobot/ncbi_files/lactos.txt")
diflen = newlen - oldlen

# Convert integers to strings
newlen_str = str(newlen)
diflen_str = str(diflen)

# Add date and count to track file
date = time.strftime("%Y%m%d")
with open("track_count.txt","a") as myfile:
	myfile.write(date + "\t" + newlen_str + "\n")

# Read in track_count file for plot
track_count = pd.read_table("/home/pi/lactobot/track_count.txt",sep="\t")

# Plot using matplotlib
ypos = np.arange(len(track_count['Date']))
plt.barh(ypos,track_count['Count'], align='center', alpha=0.4)
plt.yticks(ypos, track_count['Date'])
plt.title("Amount of Lactobacillus assemblies")
plt.savefig('image.png')

# Set up twitter credentials

apiKey = # deleted for security reasons
apiSecret = # deleted
accessToken = # deleted
accessTokenSecret = # deleted

api = Twython(apiKey,apiSecret,accessToken,accessTokenSecret)

# Set up photo and tweet
photo = open("image.png","rb")
tweetStr = "There are currently " + newlen_str + " Lactobacillus assemblies available. That's " + diflen_str + " more than yesterday. #lactobot"

# Update status only when diflen differs from 0
if diflen != 0:
	api.update_status_with_media(media=photo,status=tweetStr)
	print "Tweeted: " + tweetStr
else:
	print "I did not tweet today, because nothing interesting happened"
