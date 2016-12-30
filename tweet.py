#!/usr/bin/env python
from __future__ import print_function

import datetime

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from twython import Twython


sns.set_style("whitegrid")


def file_len(fname):
    with open(fname) as f:
        return len(f.readlines())


# Count the number of lines in new lactos file
num_lactos_new = file_len("/home/pi/lactobot/ncbi_files/lactos.txt")
today = np.datetime64(datetime.datetime.now(), "D")

# Update the stored number of assemblies
track_count = pd.Series.from_csv("track_count.txt", sep="\t", header=0, infer_datetime_format=True)
track_count.loc[today] = num_lactos_new   # don't store duplicate entries
track_count.to_csv("track_count.txt", sep="\t", header=True, index_label="Date")

# Check whether we found new assemblies compared to the previous recorded value
num_lactos_dif = num_lactos_new - int(track_count.shift(1)[today])

# Plot changes in the number of assemblies
plt.figure()

plt.plot(track_count.index, track_count, "-o")

plt.gca().yaxis.set_major_formatter(mpl.ticker.ScalarFormatter(useOffset=False))
plt.gca().margins(0.05, 0.05)

plt.xlabel("Date")
plt.ylabel("Number of Lactobacillus assemblies")
plt.title("#lactobot", size="x-large", weight="bold")

plt.savefig("image.png")
plt.close()

# Set up twitter credentials

apiKey = # deleted for security reasons
apiSecret = # deleted
accessToken = # deleted
accessTokenSecret = # deleted

api = Twython(apiKey, apiSecret, accessToken, accessTokenSecret)

# Set up photo and tweet
photo = open("image.png", "rb")
tweetStr = "There are currently {} Lactobacillus assemblies available. That's {} more than yesterday. #lactobot".format(num_lactos_new, num_lactos_dif)

# Update status only when diflen differs from 0
if num_lactos_dif != 0:
    api.update_status_with_media(media=photo, status=tweetStr)
    print("Tweeted: {}".format(tweetStr))
else:
    print("I did not tweet today, because nothing interesting happened")
